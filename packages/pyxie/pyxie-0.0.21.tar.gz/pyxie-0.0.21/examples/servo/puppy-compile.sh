#!/bin/bash

cd ../..
export PYTHONPATH=.
./bin/pyxie --profile arduino compile examples/servo/servo-test-puppy-min.pyxie
