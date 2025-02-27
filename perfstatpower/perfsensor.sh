#!/bin/bash


perf stat -a -e power/energy-pkg/ -x, -I 1000
