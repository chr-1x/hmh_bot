#!/bin/sh

cd /home/pi/dev/_local/util/willie-handmade
exec willie -k
exec git stash
exec willie
