# Plotting

Single-market plotting is built into the shared runner flow used by the public
prediction-market backtests.

Optimizer runners write search artifacts to `output/` as CSV and JSON. They do
not emit one HTML chart per trial by default.

Every public runner now exposes two explicit plotting controls at top level:

- `EMIT_HTML` keeps per-run HTML generation on or off in the file itself
- `CHART_OUTPUT_PATH` keeps the destination explicit instead of hiding it in
  shared defaults

Good examples:

- [`backtests/kalshi_trade_tick_breakout.py`](https://github.com/evan-kolberg/prediction-market-backtesting/blob/main/backtests/kalshi_trade_tick_breakout.py)
- [`backtests/kalshi_trade_tick_panic_fade.py`](https://github.com/evan-kolberg/prediction-market-backtesting/blob/main/backtests/kalshi_trade_tick_panic_fade.py)
- [`backtests/polymarket_quote_tick_pmxt_panic_fade.py`](https://github.com/evan-kolberg/prediction-market-backtesting/blob/main/backtests/polymarket_quote_tick_pmxt_panic_fade.py)
- [`backtests/polymarket_quote_tick_pmxt_vwap_reversion.py`](https://github.com/evan-kolberg/prediction-market-backtesting/blob/main/backtests/polymarket_quote_tick_pmxt_vwap_reversion.py)

## Output Paths

With `CHART_OUTPUT_PATH=None`, single-market runners keep the default
`output/<backtest>_<market>_legacy.html` naming.

If you want to override that, set:

- `CHART_OUTPUT_PATH="output/custom.html"` for one explicit file path
- `CHART_OUTPUT_PATH="output/charts"` for one explicit directory
- `CHART_OUTPUT_PATH="output/{name}_{market_id}.html"` for an explicit template

When a multi-sim runner points at a single file path, the runner appends the
market id before the suffix so repeated sims do not overwrite each other.

Charts are written to `output/`, typically with names like:

- `output/<backtest>_<market>_legacy.html`
- `output/polymarket_quote_tick_pmxt_ema_crossover_<market>_legacy.html`
- `output/polymarket_quote_tick_pmxt_breakout_<market>_legacy.html`
- `output/polymarket_quote_tick_pmxt_rsi_reversion_<market>_legacy.html`
- `output/polymarket_quote_tick_pmxt_spread_capture_<market>_legacy.html`
- `output/polymarket_quote_tick_pmxt_multi_sim_runner_combined_legacy.html`
- `output/polymarket_quote_tick_pmxt_multi_sim_runner_multi_market.html`
- `output/polymarket_quote_tick_pmxt_ema_optimizer_leaderboard.csv`
- `output/polymarket_quote_tick_pmxt_ema_optimizer_summary.json`

## Multi-Market References

The clearest multi-market plotting references are the flat Polymarket trade-tick
runner files:

- [`backtests/polymarket_trade_tick_sports_final_period_momentum.py`](https://github.com/evan-kolberg/prediction-market-backtesting/blob/main/backtests/polymarket_trade_tick_sports_final_period_momentum.py)
- [`backtests/polymarket_trade_tick_sports_vwap_reversion.py`](https://github.com/evan-kolberg/prediction-market-backtesting/blob/main/backtests/polymarket_trade_tick_sports_vwap_reversion.py)

Those runners write one combined summary chart to `output/`, typically with
names like:

- `output/polymarket_trade_tick_sports_final_period_momentum_multi_market.html`
- `output/polymarket_trade_tick_sports_vwap_reversion_multi_market.html`
