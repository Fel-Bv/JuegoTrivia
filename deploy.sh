#!/bin/bash
#-*- coding: utf8 -*-

cp -r ../venv/lib/ .

git add .
git commit
git push heroku master

