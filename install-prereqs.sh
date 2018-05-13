#!/bin/bash

git clone https://github.com/dcdanko/DataSuper.git datasuper
( cd datasuper; git checkout develop )
pip install -e datasuper
