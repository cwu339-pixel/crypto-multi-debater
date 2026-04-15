# External Upstreams

This folder holds upstream repositories or reference material that inform the local implementation.

## Boundary

Contents under `external/` are not the primary maintained source of this project. They are kept to make upstream context inspectable and to document where specific research patterns came from.

## Tracked here

- `open_deep_research/`
  - upstream: `https://github.com/langchain-ai/open_deep_research.git`
  - retained as a local upstream reference for the evidence-collection path
  - should be reviewed as vendored context rather than first-party application code

## Existing local checkouts

- TradingAgents
  - local path: `/Users/wuchenghan/Projects/TradingAgents`
  - upstream: `https://github.com/TauricResearch/TradingAgents.git`
  - pinned local commit at scaffold time: `589b351f2ab55a8a37d846848479cebc810a5a36`

## Not vendored here

- LangGraph
- OpenBB

Those stay as library dependencies for now rather than committed upstream trees.
