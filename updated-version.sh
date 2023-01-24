#!/bin/bash

now=$(date)
touch file.txt
echo "$now" > file.txt

git add updated-version.sh
git add file.txt
git commit -m "updated"
git push

