# Google Discover Feed API

Collect a sample of Google Discover cards for a country with the hosted Apify Actor. This integration guide provides no-code steps, API examples and JSON and CSV samples for editorial and SEO monitoring.

[Open Google Discover Feed Scraper on Apify](https://apify.com/datascraperes/google-discover-scraper?fpr=edudata)

## What this repository helps you do

- Track publishers, posts and videos appearing in an anonymous Discover feed.
- Compare snapshots across markets and preserve the order in which cards appeared.
- Export a saved run to CSV without starting a new collection.

## Example result

A saved video card can include a publisher label, duration and first-seen position. See the [complete JSON row](data/sample-output.json) and its [CSV representation](data/sample-output.csv).

## Run without code

1. Open the [Actor on Apify](https://apify.com/datascraperes/google-discover-scraper?fpr=edudata).
2. Under **Input**, choose a country and set **Maximum articles** to 5 for a short run.
3. Select **Start**, then open the run's **Dataset** to review or export rows.

[No-code walkthrough](docs/no-code-guide.md)

## Try it with Apify's free plan

Apify's Free plan includes **$5 of monthly prepaid usage** and requires no credit card to start. That credit can cover a small test while it remains available. [Current Apify plans](https://apify.com/pricing?fpr=edudata)

## Quick start for developers

Python 3.10+ and an Apify API token are sufficient. Supply your token through the `APIFY_API_TOKEN` environment variable.

```bash
python examples/python/fetch_feed.py
```

## Input example

```json
{
  "country": "us",
  "maxArticles": 5
}
```

[Input reference](docs/input-reference.md)

## Request examples

- [cURL](examples/curl-request.md) starts a budget-capped run and retrieves its Dataset.
- [Python single run](examples/python/fetch_feed.py) prints the Dataset and completion summary.
- [Python batch](examples/python/batch_markets.py) starts one bounded run per selected market.
- [Python CSV export](examples/python/export_csv.py) paginates through a run you already have.
- [JavaScript](examples/javascript/request.mjs) starts and verifies one run with Node.js 20+.

## Output fields

| Field | Meaning |
| --- | --- |
| `title` and `displayTitle` | Headline and optional visible headline |
| `url` and `domain` | Card destination and its domain |
| `publisherName` and `contentType` | Optional publisher label and recognized card type |
| `sampleNumber` and `positionInSample` | First observed sample and position in that sample |

[Output reference](docs/output-reference.md)

## Common use cases

[Workflow examples](docs/use-cases.md) cover publisher monitoring, country comparisons and CSV reporting.

## Monitor Google Discover by country

Run a small collection in each market and record the run ID with each snapshot. The feed rotates, so use repeated snapshots to measure appearance over time. [Batch example](examples/python/batch_markets.py)

## Export a Google Discover feed to CSV

Pass an existing Apify run ID and a destination filename to the [export example](examples/python/export_csv.py). It verifies the Dataset against the run's summary before writing.

## FAQ

[Frequently asked questions](docs/faq.md) cover country selection, varying yields and retrying safely.

## Limits and pricing

The Actor charges one pay-per-event `article` event per unique card saved. The requested maximum is a cap. The feed may run out of new cards first. The current rate ranges from **USD 0.75 to USD 1.00 per 1,000 cards**, depending on plan. Open the [Actor on Apify](https://apify.com/datascraperes/google-discover-scraper?fpr=edudata) and select **Pricing** for the current rate.

## Hosted version

[Run Google Discover Feed Scraper on Apify](https://apify.com/datascraperes/google-discover-scraper?fpr=edudata)

## Responsible use

Use the results within the terms and privacy obligations applicable to your workflow. Keep credentials outside the repository and review the charge cap before starting batches.

## Support

[Open a GitHub issue](https://github.com/datacrawler-edu/google-discover-feed-api/issues) for example bugs. Include sanitized input and the run ID for reproducible failures.

## License

The integration examples use the [MIT License](LICENSE).
