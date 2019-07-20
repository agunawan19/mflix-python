#!/bin/env bash

venv="venv"
file="requirements.txt"

if [[ ! -d $venv ]]; then
    py -m venv $venv
fi

source "./$venv/Scripts/activate"

pip install -r "./$file"
