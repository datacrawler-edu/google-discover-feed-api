"""Start and read runs of the hosted Google Discover Feed Scraper."""
import json
import os
import time
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

ACTOR = "datascraperes~google-discover-scraper"
ROOT = Path(__file__).resolve().parents[2]
TERMINAL = {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}


class RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def api(route, body=None, *, base="https://api.apify.com", token=None):
    token = token or os.environ.get("APIFY_API_TOKEN")
    if not token:
        raise SystemExit("Set APIFY_API_TOKEN to use the examples.")
    request = Request(
        base + "/v2/" + route,
        data=None if body is None else json.dumps(body).encode("utf-8"),
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
    )
    with build_opener(RejectRedirects()).open(request, timeout=25) as response:
        return json.load(response)


def start(payload, **connection):
    query = urlencode({"timeout": 120, "maxTotalChargeUsd": "0.01"})
    try:
        run_id = api(f"actors/{ACTOR}/runs?{query}", payload, **connection)["data"]["id"]
        if not isinstance(run_id, str) or not run_id:
            raise ValueError("Missing run ID")
        return run_id
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise RuntimeError("Start was not confirmed. Inspect Apify run history before retrying.") from error


def fetch_result(run_id, *, page_size=100, **connection):
    route = "actor-runs/" + quote(run_id, safe="")
    deadline = time.monotonic() + 180
    while time.monotonic() < deadline:
        run = api(route + "?waitForFinish=10", **connection)["data"]
        if run["status"] in TERMINAL:
            break
        time.sleep(1)
    else:
        raise TimeoutError(f"Continue checking the existing run {run_id}.")
    store = quote(run["defaultKeyValueStoreId"], safe="")
    summary = api(f"key-value-stores/{store}/records/SUMMARY", **connection)
    expected = summary.get("articlesDelivered")
    if type(expected) is not int or not 0 <= expected <= 1000:
        raise RuntimeError(f"Unverified saved row count for run {run_id}.")
    dataset = quote(run["defaultDatasetId"], safe="")
    rows = []
    for offset in range(0, expected + 1, page_size):
        query = urlencode({"offset": offset, "limit": page_size})
        page = api(f"datasets/{dataset}/items?{query}", **connection)
        rows.extend(page)
        if len(page) < page_size:
            break
    if len(rows) != expected or len({row["url"] for row in rows}) != expected:
        raise RuntimeError(f"The Dataset and SUMMARY disagree for run {run_id}.")
    return {"runId": run_id, "platformStatus": run["status"], "summary": summary, "cards": rows}


def sample_input():
    return json.loads((ROOT / "data/sample-input.json").read_text(encoding="utf-8"))
