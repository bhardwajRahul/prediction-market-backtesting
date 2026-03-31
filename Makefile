.PHONY: backtest install update test clear-pmxt-cache

PMXT_CACHE_ROOT ?= $(if $(XDG_CACHE_HOME),$(XDG_CACHE_HOME),$(HOME)/.cache)/nautilus_trader/pmxt

backtest:
	uv run python main.py

install:
	unset CONDA_PREFIX && uv venv --python 3.13 && uv pip install -e nautilus_pm/ bokeh plotly numpy py-clob-client duckdb

test:
	uv run pytest tests/ -v

clear-pmxt-cache:
	rm -rf "$(PMXT_CACHE_ROOT)"
	mkdir -p "$(PMXT_CACHE_ROOT)"
	du -sh "$(PMXT_CACHE_ROOT)"

update:
	git subtree pull --prefix=nautilus_pm https://github.com/ben-gramling/nautilus_pm.git charting --squash
