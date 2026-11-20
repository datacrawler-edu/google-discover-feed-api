"""Print one small Google Discover run and its summary as JSON."""
import json

from request import fetch_result, sample_input, start


if __name__ == "__main__":
    run_id = start(sample_input())
    print(json.dumps(fetch_result(run_id), ensure_ascii=False, indent=2))
