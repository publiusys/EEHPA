#!/usr/bin/env bash
set -e

kubectl exec --stdin --tty $1 -- /bin/bash
