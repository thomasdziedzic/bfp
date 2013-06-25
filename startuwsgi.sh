#!/bin/sh

uwsgi --http :5000 --wsgi-file bfp.py --callable app
