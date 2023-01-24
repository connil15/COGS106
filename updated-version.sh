#!/bin/bash

now=$(date)
touch file.txt
echo "$now" > file.txt

git add updated-version.sh
git commit -m "updated"
git push

