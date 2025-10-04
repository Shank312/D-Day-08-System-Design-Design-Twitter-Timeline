

SHELL := /bin/bash

.PHONY: dev down lint test fmt

dev:
\tdocker compose -f deploy/docker-compose.yml up -d --build

down:
\tdocker compose -f deploy/docker-compose.yml down -v

lint:
\tpython -m pip install ruff==0.6.9 && ruff check services shared

fmt:
\tpython -m pip install ruff==0.6.9 && ruff format services shared

test:
\tpytest -q
