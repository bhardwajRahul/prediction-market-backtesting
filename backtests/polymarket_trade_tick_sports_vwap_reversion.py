# Derived from NautilusTrader prediction-market example code.
# Distributed under the GNU Lesser General Public License Version 3.0 or later.
# Modified in this repository on 2026-03-11, 2026-03-16, and 2026-04-03.
# See the repository NOTICE file for provenance and licensing scope.

"""
VWAP reversion on a fixed Polymarket sports basket using native trade ticks.
"""

# ruff: noqa: E402

from __future__ import annotations

from decimal import Decimal

from _script_helpers import ensure_repo_root

ensure_repo_root(__file__)

from backtests._shared._prediction_market_backtest import MarketReportConfig
from backtests._shared._prediction_market_backtest import MarketSimConfig
from backtests._shared._prediction_market_backtest import PredictionMarketBacktest
from backtests._shared._prediction_market_backtest import finalize_market_results
from backtests._shared._prediction_market_runner import MarketDataConfig
from backtests._shared._timing_harness import timing_harness
from backtests._shared.data_sources import Native, Polymarket, TradeTick


NAME = "polymarket_trade_tick_sports_vwap_reversion"

DESCRIPTION = "VWAP reversion on a fixed Polymarket sports basket"

DATA = MarketDataConfig(
    platform=Polymarket,
    data_type=TradeTick,
    vendor=Native,
    sources=(
        "gamma=https://gamma-api.polymarket.com",
        "trades=https://data-api.polymarket.com",
        "clob=https://clob.polymarket.com",
    ),
)

SIMS = (
    MarketSimConfig(
        market_slug="will-ukraine-qualify-for-the-2026-fifa-world-cup",
        outcome="Yes",
    ),
    MarketSimConfig(
        market_slug="will-man-city-win-the-202526-champions-league",
        outcome="Yes",
    ),
    MarketSimConfig(
        market_slug="will-chelsea-win-the-202526-champions-league",
        outcome="Yes",
    ),
    MarketSimConfig(
        market_slug="will-newcastle-win-the-202526-champions-league",
        outcome="Yes",
    ),
    MarketSimConfig(
        market_slug="will-leverkusen-win-the-202526-champions-league",
        outcome="Yes",
    ),
)

STRATEGY_CONFIGS = [
    {
        "strategy_path": "strategies:TradeTickVWAPReversionStrategy",
        "config_path": "strategies:TradeTickVWAPReversionConfig",
        "config": {
            "trade_size": Decimal("100"),
            "vwap_window": 80,
            "entry_threshold": 0.02,
            "exit_threshold": 0.004,
            "min_tick_size": 10.0,
            "take_profit": 0.03,
            "stop_loss": 0.02,
        },
    },
]

REPORT = MarketReportConfig(
    count_key="trades",
    count_label="Trades",
    pnl_label="PnL (USDC)",
)

BACKTEST = PredictionMarketBacktest(
    name=NAME,
    data=DATA,
    sims=SIMS,
    strategy_configs=STRATEGY_CONFIGS,
    initial_cash=100.0,
    probability_window=80,
    min_trades=25,
    min_price_range=0.05,
    default_lookback_days=30,
)


@timing_harness
def run() -> None:
    results = BACKTEST.run()
    if not results:
        print("No fixed Polymarket sports sims met the trade-tick requirements.")
        return

    if len(results) < len(SIMS):
        print(f"Completed {len(results)} of {len(SIMS)} fixed sports sims.")

    finalize_market_results(name=NAME, results=results, report=REPORT)


if __name__ == "__main__":
    run()
