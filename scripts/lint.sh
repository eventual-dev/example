#!/bin/sh -e

export SOURCE_FILES="example tests"
set -x

autoflake --in-place --recursive $SOURCE_FILES
isort --project=example $SOURCE_FILES
black $SOURCE_FILES
