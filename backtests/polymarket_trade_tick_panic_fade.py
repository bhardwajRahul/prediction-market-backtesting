# Derived from NautilusTrader prediction-market example code.
# Distributed under the GNU Lesser General Public License Version 3.0 or later.
# Modified in this repository on 2026-03-11.
# See the repository NOTICE file for provenance and licensing scope.

"""
Panic-fade strategy on one Polymarket market.
"""

# ruff: noqa: E402

from __future__ import annotations

from decimal import Decimal

from _script_helpers import ensure_repo_root

ensure_repo_root(__file__)

from backtests._shared._prediction_market_backtest import MarketReportConfig
from backtests._shared._prediction_market_backtest import MarketSimConfig
from backtests._shared._prediction_market_backtest import PredictionMarketBacktest
from backtests._shared._prediction_market_backtest import run_reported_backtest
from backtests._shared._prediction_market_runner import MarketDataConfig
from backtests._shared._timing_harness import timing_harness
from backtests._shared.data_sources import Native, Polymarket, TradeTick


NAME = "polymarket_trade_tick_panic_fade"

DESCRIPTION = "Panic selloff fade strategy on a single Polymarket market"

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
        market_slug="will-openai-launch-a-new-consumer-hardware-product-by-march-31-2026",
        lookback_days=30,
    ),
)

STRATEGY_CONFIGS = [
    {
        "strategy_path": "strategies:TradeTickPanicFadeStrategy",
        "config_path": "strategies:TradeTickPanicFadeConfig",
        "config": {
            "trade_size": Decimal("100"),
            "drop_window": 30,
            "min_drop": 0.002,
            "panic_price": 0.249,
            "rebound_exit": 0.251,
            "max_holding_periods": 80,
            "take_profit": 0.004,
            "stop_loss": 0.004,
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
    probability_window=30,
    min_trades=300,
    min_price_range=0.005,
)


@timing_harness
def run() -> None:
    run_reported_backtest(
        backtest=BACKTEST,
        report=REPORT,
        empty_message="No Polymarket panic-fade sims met the trade-tick requirements.",
    )


if __name__ == "__main__":
    run()
