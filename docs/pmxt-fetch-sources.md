# PMXT Data Fetch Sources and Timing

When running a backtest, the PMXT loader fetches historical L2 order book data one hour at a time. Each hour can come from one of three sources, tried in order:

1. **Local cache** (`~/.cache/nautilus_trader/pmxt/...`) — cached from a previous run. Sub-millisecond.
2. **Relay prebuilt** (`https://209-209-10-83.sslip.io`) — pre-partitioned per market/token file served directly. Under 2 seconds.
3. **Relay fallback** (same URL) — the hour exists on the relay but hasn't been prebuilt yet. The relay scans the full processed parquet (all markets in that hour) and filters server-side. 30-65 seconds.
4. **Raw PMXT archive** (`https://r2.pmxt.dev`) — the hour isn't on the relay at all. Downloads the entire raw archive file and filters client-side. 30+ seconds.

If a source fails or returns nothing, the loader falls through to the next one. After a successful fetch from sources 2-4, the result is written to the local cache so subsequent runs are instant.

Caching is enabled by default at `~/.cache/nautilus_trader/pmxt/`. To disable it, set `PMXT_DISABLE_CACHE=true`.

## Example output

This is real output from a 96-hour deep value backtest on the `will-openai-launch-a-new-consumer-hardware-product-by-march-31-2026` market, run on 2026-03-24. It shows all four source tiers in a single run:

```
Loading PMXT Polymarket market will-openai-launch-a-new-consumer-hardware-product-by-march-31-2026
(token_index=0, lookback=96.0h, window_end=2026-03-24T07:04:55.299246+00:00)...
```

### Relay fallback (not yet prebuilt)

These hours exist on the relay as processed parquets but haven't been split into per-market files yet. The relay scans the full hour on the fly, which takes 30-65s depending on hour density:

```
  2026-03-20T18:00:00+00:00  39.725s      25 rows  https://209-209-10-83.sslip.io
  2026-03-20T13:00:00+00:00  39.731s     358 rows  https://209-209-10-83.sslip.io
  2026-03-20T20:00:00+00:00  39.774s    1342 rows  https://209-209-10-83.sslip.io
  2026-03-20T16:00:00+00:00  39.779s     161 rows  https://209-209-10-83.sslip.io
  2026-03-20T07:00:00+00:00  39.782s     610 rows  https://209-209-10-83.sslip.io
  2026-03-20T19:00:00+00:00  39.791s      33 rows  https://209-209-10-83.sslip.io
  2026-03-20T09:00:00+00:00  39.792s     516 rows  https://209-209-10-83.sslip.io
  2026-03-20T17:00:00+00:00  39.796s     396 rows  https://209-209-10-83.sslip.io
  2026-03-20T06:00:00+00:00  39.803s      73 rows  https://209-209-10-83.sslip.io
  2026-03-20T10:00:00+00:00  44.557s     292 rows  https://209-209-10-83.sslip.io
  2026-03-20T15:00:00+00:00  44.674s     390 rows  https://209-209-10-83.sslip.io
  2026-03-20T12:00:00+00:00  48.507s     392 rows  https://209-209-10-83.sslip.io
  2026-03-20T08:00:00+00:00  53.424s    3201 rows  https://209-209-10-83.sslip.io
  2026-03-20T14:00:00+00:00  62.578s     183 rows  https://209-209-10-83.sslip.io
  2026-03-20T21:00:00+00:00  63.597s    2961 rows  https://209-209-10-83.sslip.io
  2026-03-20T11:00:00+00:00  65.841s      71 rows  https://209-209-10-83.sslip.io
```

Note: the time doesn't correlate with row count. A 25-row hour and a 1342-row hour both take ~40s because the bottleneck is scanning the full processed parquet (all markets), not returning the filtered result.

### Relay prebuilt

These hours have been fully prebuilt on the relay (split into per-market/token files). The relay serves the small pre-filtered file directly:

```
  2026-03-20T22:00:00+00:00   4.867s     687 rows  https://209-209-10-83.sslip.io
  2026-03-20T23:00:00+00:00  12.850s    2463 rows  https://209-209-10-83.sslip.io
  2026-03-21T01:00:00+00:00   2.125s      17 rows  https://209-209-10-83.sslip.io
  2026-03-21T05:00:00+00:00   1.637s      91 rows  https://209-209-10-83.sslip.io
  2026-03-21T03:00:00+00:00   1.694s     227 rows  https://209-209-10-83.sslip.io
```

The variation (1.6-12.8s) is from network conditions and concurrent prefetch batching, not file size.

### Some hours fell back to the relay fallback despite being surrounded by prebuilt hours

The relay prebuilds newest-first, so there can be gaps where recent hours are prebuilt but slightly older ones aren't yet:

```
  2026-03-21T02:00:00+00:00  36.685s       7 rows  https://209-209-10-83.sslip.io
  2026-03-21T00:00:00+00:00  37.406s     582 rows  https://209-209-10-83.sslip.io
  2026-03-21T04:00:00+00:00  26.956s     300 rows  https://209-209-10-83.sslip.io
```

### Local cache hits (from a previous run)

These hours were fetched in an earlier backtest run and cached locally. Sub-millisecond reads:

```
  2026-03-21T13:00:00+00:00   0.032s      60 rows  /Users/evankolberg/.cache/nautilus_trader/pmxt/0xe967.../6949.../polymarket_orderbook_2026-03-21T13.parquet
  2026-03-21T06:00:00+00:00   0.046s     458 rows  /Users/evankolberg/.cache/nautilus_trader/pmxt/0xe967.../6949.../polymarket_orderbook_2026-03-21T06.parquet
  2026-03-21T09:00:00+00:00   0.027s     145 rows  /Users/evankolberg/.cache/nautilus_trader/pmxt/0xe967.../6949.../polymarket_orderbook_2026-03-21T09.parquet
  2026-03-21T15:00:00+00:00   0.002s      23 rows  /Users/evankolberg/.cache/nautilus_trader/pmxt/0xe967.../6949.../polymarket_orderbook_2026-03-21T15.parquet
  2026-03-22T14:00:00+00:00   0.001s      20 rows  /Users/evankolberg/.cache/nautilus_trader/pmxt/0xe967.../6949.../polymarket_orderbook_2026-03-22T14.parquet
```

### Raw PMXT archive fallback

This hour wasn't available on the relay at all (too recent, not yet mirrored). The loader fell back to the raw PMXT archive at `r2.pmxt.dev`, downloading the full hour file and filtering client-side:

```
  2026-03-24T06:00:00+00:00  32.293s      40 rows  https://r2.pmxt.dev
```

### Hour not found anywhere

This hour didn't exist on any source (future hour, no data yet):

```
  2026-03-24T07:00:00+00:00   0.570s       0 rows  none
```

### Final result

```
Fetching hours: 100%|████████████████████████████████████| 98/98 [02:05<00:00]

Market                                                                  Quotes  Fills   PnL (USDC)
will-openai-launch-a-new-consumer-hardware-product-by-march-31-2026      20303      2      -1.4480

Total wall time: 127.89s
```

98 hours fetched in ~2 minutes. The bulk of that time was spent on the ~20 non-prebuilt hours hitting relay fallback. On a second run, every hour comes from cache and the same backtest completes in under a second.

## Timing expectations by source

| Source | Typical time | When it happens |
|---|---|---|
| Local cache | <0.05s | Second run onward (same market/token/hour) |
| Relay prebuilt | 0.5-3s | Hour has been fully prebuilt on the relay |
| Relay fallback | 30-65s | Hour is processed but not yet prebuilt |
| Raw PMXT archive | 30+s | Hour not on the relay (too recent or relay down) |
| None | <1s | Hour doesn't exist yet |

## How to see this output

The timing instrumentation is built into `make backtest` (via `main.py`). It can also be run standalone against any backtest file:

```bash
uv run python backtests/_timing_test.py backtests/polymarket_pmxt_relay_ema_crossover.py
```

Environment variables control the market and window:

```bash
MARKET_SLUG=some-market LOOKBACK_HOURS=80 END_TIME=2026-03-24T04:00:00Z \
    uv run python backtests/_timing_test.py backtests/polymarket_pmxt_relay_breakout.py
```
