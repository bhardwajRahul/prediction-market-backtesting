# prediction-market-backtesting

![GitHub stars](https://img.shields.io/github/stars/evan-kolberg/prediction-market-backtesting?style=social)
![GitHub forks](https://img.shields.io/github/forks/evan-kolberg/prediction-market-backtesting?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/evan-kolberg/prediction-market-backtesting?style=social)

[![Licensing: Mixed](https://img.shields.io/badge/licensing-MIT%20%2B%20LGPL--3.0--or--later-blue.svg)](NOTICE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)
![Rust](https://img.shields.io/badge/rust-1.93.1-CE422B?logo=rust&logoColor=white)
![Rust Edition](https://img.shields.io/badge/edition-2024-CE422B?logo=rust&logoColor=white)
![NautilusTrader](https://img.shields.io/badge/NautilusTrader-1.224.0-1E3A5F)
![GitHub last commit](https://img.shields.io/github/last-commit/evan-kolberg/prediction-market-backtesting)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/evan-kolberg/prediction-market-backtesting)
![GitHub code size](https://img.shields.io/github/languages/code-size/evan-kolberg/prediction-market-backtesting)
![GitHub top language](https://img.shields.io/github/languages/top/evan-kolberg/prediction-market-backtesting)
![GitHub open issues](https://img.shields.io/github/issues/evan-kolberg/prediction-market-backtesting)

Relay VPS statistics:

[![PMXT relay](https://209-209-10-83.sslip.io/v1/badge/status.svg)](https://209-209-10-83.sslip.io/v1/stats)
[![Relay CPU](https://209-209-10-83.sslip.io/v1/badge/cpu.svg)](https://209-209-10-83.sslip.io/v1/system)
[![Relay mem](https://209-209-10-83.sslip.io/v1/badge/mem.svg)](https://209-209-10-83.sslip.io/v1/system)
[![Relay disk](https://209-209-10-83.sslip.io/v1/badge/disk.svg)](https://209-209-10-83.sslip.io/v1/system)

[![PMXT mirrored](https://209-209-10-83.sslip.io/v1/badge/mirrored.svg)](https://209-209-10-83.sslip.io/v1/stats)
[![PMXT processed](https://209-209-10-83.sslip.io/v1/badge/processed.svg)](https://209-209-10-83.sslip.io/v1/stats)
[![PMXT latest](https://209-209-10-83.sslip.io/v1/badge/latest.svg?v=3)](https://209-209-10-83.sslip.io/v1/queue)
[![PMXT lag](https://209-209-10-83.sslip.io/v1/badge/lag.svg?v=3)](https://209-209-10-83.sslip.io/v1/queue)
[![PMXT rate](https://209-209-10-83.sslip.io/v1/badge/rate.svg?v=1)](https://209-209-10-83.sslip.io/v1/stats)

[![PMXT file](https://209-209-10-83.sslip.io/v1/badge/prebuild-file.svg?v=1)](https://209-209-10-83.sslip.io/v1/events?limit=50)
[![PMXT rows](https://209-209-10-83.sslip.io/v1/badge/prebuild-progress.svg?v=1)](https://209-209-10-83.sslip.io/v1/events?limit=50)

Backtesting framework for prediction market strategies on
[Kalshi](https://kalshi.com) and [Polymarket](https://polymarket.com), built on
top of [NautilusTrader](https://github.com/nautechsystems/nautilus_trader) with
custom exchange adapters. Plotting is inspired by [minitrade](https://github.com/dodid/minitrade). This repo is still in active development, and a full release should happen within the next one to two months..

![Charting preview](https://raw.githubusercontent.com/evan-kolberg/prediction-market-backtesting/main/docs/assets/charting-preview.jpeg)

## Table of Contents

- `docs/`
  - `├──` [index.md](docs/index.md) - Docs Index
  - `├──` [setup.md](docs/setup.md) - Setup
  - `├──` [backtests.md](docs/backtests.md) - Backtests And Runners
  - `├──` [execution-modeling.md](docs/execution-modeling.md) - Execution Modeling
  - `├──` [pmxt-byod.md](docs/pmxt-byod.md) - PMXT BYOD And Local Data
  - `├──` [pmxt-fetch-sources.md](docs/pmxt-fetch-sources.md) - PMXT Fetch Sources And Timing
  - `├──` [pmxt-relay.md](docs/pmxt-relay.md) - PMXT Relay
  - `├──` [plotting.md](docs/plotting.md) - Plotting
  - `├──` [testing.md](docs/testing.md) - Testing
  - `├──` [project-status.md](docs/project-status.md) - Project Status
  - `└──` [license.md](docs/license.md) - License Notes


## Star History

<a href="https://www.star-history.com/?repos=evan-kolberg%2Fprediction-market-backtesting&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=evan-kolberg/prediction-market-backtesting&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=evan-kolberg/prediction-market-backtesting&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/image?repos=evan-kolberg/prediction-market-backtesting&type=date&legend=top-left" />
 </picture>
</a>
