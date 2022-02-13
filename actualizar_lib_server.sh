#!/bin/bash
#-*- coding: utf8 -*-

echo -en "\x1b[1;34mCopiando archivos... \x1b[0m"
cp -r lib/* /app/.heroku/python/lib/python3.8/site-packages/
echo -e "\x1b[1;32mListo\x1b[0m"

