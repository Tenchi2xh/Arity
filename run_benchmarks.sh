#!/bin/sh

PYTEST=pytest
if ! type -P "$PYTEST" > /dev/null; then
  PYTEST=py.test
fi
PYTHONPATH=. $PYTEST benchmarks -v # --benchmark-warmup-iterations 1 --benchmark-max-time 2
