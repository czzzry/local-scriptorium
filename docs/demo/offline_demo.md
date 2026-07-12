# Offline Demonstration

```console
$ scriptorium ingest
.../outputs/generated/corpus.v1.json

$ scriptorium retrieve "How is providence distinguished from fate?" --method bm25
{
  "schema_version": "1.0",
  "method": "bm25",
  "results": [
    {"chunk_id": "BOETHIUS_CONSOLATION_001_CHUNK_055", "rank": 1, "score": "..."}
  ]
}

$ scriptorium evaluate --split test --deterministic
.../outputs/generated/retrieval_results.json

$ scriptorium report
.../outputs/generated/report.md
```

The retrieved chunk states that providence is the unified divine foreview while fate is that order unfolded through time. A cited answer may use that distinction and cite `...CHUNK_055`; it should not add historical or theological claims absent from retrieved evidence.

