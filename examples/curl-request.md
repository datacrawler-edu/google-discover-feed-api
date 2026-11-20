# Run and read the hosted Actor with cURL

Set `APIFY_API_TOKEN` in your shell. Run this command once from the repository root:

```bash
curl --fail-with-body --max-time 30 -X POST \
  -H "Authorization: Bearer ${APIFY_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data-binary @data/sample-input.json \
  "https://api.apify.com/v2/actors/datascraperes~google-discover-scraper/runs?timeout=120&maxTotalChargeUsd=0.01"
```

Capture `data.id` as the run ID. If the start response is lost, inspect the Actor's run history before retrying.

```bash
curl --fail-with-body -H "Authorization: Bearer ${APIFY_API_TOKEN}" \
  "https://api.apify.com/v2/actor-runs/${RUN_ID}?waitForFinish=10"
```

Repeat the **GET** above until the run is terminal. Use `data.defaultDatasetId` and `data.defaultKeyValueStoreId` from that run.

```bash
curl --fail-with-body -H "Authorization: Bearer ${APIFY_API_TOKEN}" \
  "https://api.apify.com/v2/datasets/${DATASET_ID}/items?format=json&offset=0&limit=100"
curl --fail-with-body -H "Authorization: Bearer ${APIFY_API_TOKEN}" \
  "https://api.apify.com/v2/key-value-stores/${KVS_ID}/records/SUMMARY"
```

For larger datasets, page by offset until a page is shorter than the limit. Compare the saved row count against `articlesDelivered`.
