import json
import re
from collections import Counter
from pathlib import Path


def _expected_from_log(log_path: Path):
    paths, ips, total = Counter(), set(), 0
    with log_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1

    if not paths:
        return total, len(ips), {""}

    max_count = max(paths.values())
    top_paths = {path for path, count in paths.items() if count == max_count}
    return total, len(ips), top_paths


def _load_report():
    report_path = Path("/app/report.json")
    assert report_path.exists(), "no report.json found"
    assert report_path.stat().st_size > 0, "report.json is empty"
    with report_path.open() as f:
        return json.load(f)


def test_criterion_1_output_is_valid_json():
    """Success criterion 1: the output file must be valid JSON."""
    data = _load_report()
    assert isinstance(data, dict), "report must decode to a JSON object"


def test_criterion_2_exact_fields_and_types():
    """Success criterion 2: output contains exact fields and expected types."""
    data = _load_report()

    assert set(data.keys()) == {"total_requests", "unique_ips", "top_path"}, (
        "report must contain exactly total_requests, unique_ips, and top_path"
    )
    assert isinstance(data["total_requests"], int), "total_requests must be an int"
    assert isinstance(data["unique_ips"], int), "unique_ips must be an int"
    assert isinstance(data["top_path"], str), "top_path must be a string"


def test_criterion_3_path_parsing_rule_is_respected():
    """Success criterion 3: top_path is computed from the specified HTTP request regex."""
    data = _load_report()
    _, _, top_candidates = _expected_from_log(Path("/app/access.log"))
    assert data["top_path"] in top_candidates, "top_path does not match parsed request-path frequencies"


def test_criterion_4_empty_path_case_is_supported():
    """Success criterion 4: if no request path is found, top_path must be empty."""
    data = _load_report()
    _, _, top_candidates = _expected_from_log(Path("/app/access.log"))
    if top_candidates == {""}:
        assert data["top_path"] == "", "top_path must be empty when no request path exists"


def test_criterion_5_ties_are_accepted_and_counts_match():
    """Success criterion 5: any tied top_path is accepted; counts must still match the log."""
    data = _load_report()
    expected_total, expected_unique, top_candidates = _expected_from_log(Path("/app/access.log"))

    assert data["total_requests"] == expected_total, "incorrect total_requests"
    assert data["unique_ips"] == expected_unique, "incorrect unique_ips"
    assert data["top_path"] in top_candidates, "top_path is not one of the valid top paths"
