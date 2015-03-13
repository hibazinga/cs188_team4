#!/bin/sh

iptables -I INPUT -p tcp --syn --dport 80 -m connlimit --connlimit-above 500 -j REJECT
