#!/bin/sh
pip install supervisor || yum install supervisor
cp supervisord.conf /etc
touch /var/run/supervisor.sock
mkdir -p /data/logs/supervisor
