#!/bin/bash

# if spurious-discovery-tests directory does not exist, clone it
if [ ! -d "spurious-discovery-tests" ]; then
    git clone https://github.com/magland/spurious-discovery-tests.git
fi
cd spurious-discovery-tests
git pull
cd ..