# Output reference

Each Dataset row represents one unique card. The [sample](../data/sample-output.json) shows the full row shape.

| Field | Meaning |
| --- | --- |
| `type` | Every dataset item is one Discover article card. |
| `position` | 1-based order in which the article was saved during the run. |
| `cardId` | Google's internal card marker for this feed card, when present. |
| `title` | Headline from the Discover card's annotation. |
| `displayTitle` | Headline from the card's display data, which can be longer than title. |
| `url` | Publisher article URL from the Discover card. |
| `domain` | Hostname of the article URL without a leading www. |
| `publisherName` | Publisher, channel or creator name shown on the card. |
| `contentType` | Content type derived from a recognized Discover card template. |
| `publishedAt` | Document creation timestamp reported by Google for the card, in UTC. |
| `language` | Language code Google attaches to the card content. |
| `displayAge` | Relative age as displayed by Discover, for example 5h or 2d. |
| `videoDurationSeconds` | Duration derived from the duration shown on a video card. |
| `imageUrl` | Thumbnail image served by Google for the card. |
| `faviconUrl` | Publisher favicon served by Google for the card. |
| `categoryId` | Google's internal content category identifier for the card. |
| `channelId` | Google's internal source-channel identifier for the card. |
| `contentSourceId` | Google's internal content-source identifier for the article. |
| `bundleType` | Google's internal bundle type for the card layout. |
| `uiType` | Google's internal presentation type for the card. |
| `collectedAt` | UTC timestamp when the article was saved. |
| `sampleNumber` | 1-based sample number at which the card was first saved. |
| `positionInSample` | 1-based position among extracted cards in the sample before deduplication. |

The default key-value-store record `SUMMARY` includes `status`, `articlesDelivered`, `feedSamples` and `stopReason`. Check it together with the platform status.
