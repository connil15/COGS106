#!/bin/bash

git pull

now=$(date)
touch version
echo "$now" > version

git add updated-version.sh
git add version
git commit -m "updated"
git push
