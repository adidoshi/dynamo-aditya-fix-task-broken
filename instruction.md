Read `/app/access.log` and write a JSON summary report to `/app/report.json`.

Success criteria:

1. The output file must be valid JSON.
2. The output must be a JSON object with exactly these fields:
   - `total_requests`: integer count of non-empty log lines.
   - `unique_ips`: integer count of unique client IPs (first token of each non-empty line).
   - `top_path`: most frequently requested HTTP path as a string.
3. For request parsing, count paths matched by this request pattern in each line:
   `"(GET|POST|PUT|DELETE|HEAD|PATCH) <path> HTTP/..."`.
4. If no request path is found in the log, set `top_path` to an empty string.
5. If multiple paths tie for most frequent, any tied path is accepted.
