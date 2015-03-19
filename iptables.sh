#!/bin/sh

iptables -I INPUT -p tcp --syn --dport 80 -m connlimit --connlimit-above 1000 -j REJECT
