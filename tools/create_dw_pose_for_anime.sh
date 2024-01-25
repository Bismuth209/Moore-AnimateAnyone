#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <b>"
    exit 1
fi

b=$1

for ((a=0; a<b; a++))
do
    python create_dw_pose_for_anime.py $a $b &
done