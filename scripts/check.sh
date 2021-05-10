#!/bin/sh -e

export SOURCE_FILES="example tests"
set -x

black --check --diff $SOURCE_FILES
flake8 $SOURCE_FILES
mypy $SOURCE_FILES
isort --check --diff --project=example $SOURCE_FILES
