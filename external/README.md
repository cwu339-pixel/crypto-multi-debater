# External Upstreams

This folder holds upstream repositories or references that inform the local implementation.

## Tracked here

- `open_deep_research/`
  - tracked as a git submodule
  - upstream: `https://github.com/langchain-ai/open_deep_research.git`

## Existing local checkouts

- TradingAgents
  - local path: `/Users/wuchenghan/Projects/TradingAgents`
  - upstream: `https://github.com/TauricResearch/TradingAgents.git`
  - pinned local commit at scaffold time: `589b351f2ab55a8a37d846848479cebc810a5a36`

## Not vendored yet

- LangGraph
- OpenBB

Those stay as library dependencies for now. If you want, they can be added later as explicit checkouts too.
