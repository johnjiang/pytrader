#!/usr/bin/env sh

#Using a fork that I make at https://github.com/johnjiang/pyconcordion

export PYTHONPATH=${PYTHONPATH}:./..

python /usr/local/bin/concordion_runner ./concordion -o ../dist/