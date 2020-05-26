#!/usr/bin/env bash

function main {
  set -e
  cd "/pa" || exit 1
  ls -l
  make init
  make run-preprocessing
  make run-prod
}

main
