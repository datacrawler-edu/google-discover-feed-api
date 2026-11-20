# FAQ

## Does this reproduce a signed-in user's feed?

The hosted Actor collects an anonymous sample for the selected market. Results can change between calls.

## Why did I receive fewer cards than the cap?

The Actor stops when the feed stops returning new cards or the run reaches a limit. Compare `articlesDelivered` and `stopReason` in `SUMMARY`.

## Can I export without creating another paid run?

Yes. Use the [CSV example](../examples/python/export_csv.py) with an existing run ID.

## What happens if the start response is lost?

Inspect the Actor's run history before retrying. The examples send a single POST per attempted run and never repeat an ambiguous start automatically.
