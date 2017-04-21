#!/usr/bin/env bash
python sample_addrs.py
date="2013-03-12"
mkdir ../blockparser/temp/$date
cp ../blockparser/csv/addrs* ../blockparser/temp/$date
cp ../blockparser/csv/user_edge* ../blockparser/temp/$date
