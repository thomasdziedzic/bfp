#!/bin/sh

uwsgi --wsgi-file bfp.py --callable app -s /tmp/uwsgi.sock -C -M -A 4 -m
