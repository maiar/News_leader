#!/bin/bash
# for i in 05 06 07 08 09 10 11 12
# for i in 05
for i in 01 02 03 04 05 06 07 08 09 10 11 12
do
    # aws s3 cp s3://gdelt-open-data/v2/events/ s3://liangchun-bucket/year2019/$i/ --recursive --exclude "*" --include "2019$i????????.export.csv"
    # aws s3 cp s3://gdelt-open-data/v2/mentions/ s3://liangchun-bucket/year2019/$i/ --recursive --exclude "*" --include "2019$i????????.mentions.csv"
    aws s3 cp http://data.gdeltproject.org/gdeltv2/ s3://liangchun-bucket/year2019/$i/ --recursive --exclude "*" --include "2019$i????????.export.csv"
    aws s3 cp http://data.gdeltproject.org/gdeltv2/ s3://liangchun-bucket/year2019/$i/ --recursive --exclude "*" --include "2019$i????????.mentions.csv"
done