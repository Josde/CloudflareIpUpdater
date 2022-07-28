#!/bin/bash
cd "${0%/*}" # change to script dir
source venv/script/activate
python main.py
