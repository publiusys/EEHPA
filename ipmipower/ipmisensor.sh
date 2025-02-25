#!/bin/bash

#sudo apt install ipmitool

sudo ipmitool sensor | grep Watts
