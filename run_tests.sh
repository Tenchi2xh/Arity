#!/bin/sh

PYTEST=pytest
if ! type -P "$PYTEST" > /dev/null; then
  PYTEST=py.test
fi
PYTHONPATH=. $PYTEST tests -v --cov-report term-missing --cov=arity
