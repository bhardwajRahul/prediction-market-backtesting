# Derived from NautilusTrader prediction-market example code.
# Distributed under the GNU Lesser General Public License Version 3.0 or later.
# Modified in this repository on 2026-03-11.
# See the repository NOTICE file for provenance and licensing scope.

"""
Breakout strategy on one Kalshi market.

Defaults to KXNEXTIRANLEADER-45JAN01-MKHA
and uses a 30-day trade-tick lookback.
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
from backtests._shared.data_sources import Kalshi, Native, TradeTick


NAME = "kalshi_trade_tick_breakout"

DESCRIPTION = "Volatility breakout strategy on a single Kalshi market using trade ticks"

DATA = MarketDataConfig(
    platform=Kalshi,
    data_type=TradeTick,
    vendor=Native,
    sources=("https://api.elections.kalshi.com/trade-api/v2",),
)

SIMS = (
    MarketSimConfig(
        market_ticker="KXNEXTIRANLEADER-45JAN01-MKHA",
        lookback_days=30,
    ),
)

STRATEGY_CONFIGS = [
    {
        "strategy_path": "strategies:TradeTickBreakoutStrategy",
        "config_path": "strategies:TradeTickBreakoutConfig",
        "config": {
            "trade_size": Decimal("1"),
            "window": 60,
            "breakout_std": 1.35,
            "max_entry_price": 0.9,
            "take_profit": 0.025,
            "stop_loss": 0.02,
        },
    },
]

REPORT = MarketReportConfig(
    count_key="trades",
    count_label="Trades",
    pnl_label="PnL (USD)",
)

BACKTEST = PredictionMarketBacktest(
    name=NAME,
    data=DATA,
    sims=SIMS,
    strategy_configs=STRATEGY_CONFIGS,
    initial_cash=100.0,
    probability_window=60,
    min_trades=1000,
    min_price_range=0.03,
)


@timing_harness
def run() -> None:
    run_reported_backtest(
        backtest=BACKTEST,
        report=REPORT,
        empty_message="No Kalshi breakout sims met the trade-tick requirements.",
    )


if __name__ == "__main__":
    run()
