for i in 01 02 03 04
do
	python3 combineS3Files.py --bucket 'liangchun-bucket' --folder 'year2019/$i' --suffix '.export.csv' --output 'data/events.csv$i' --filesize 1000000000
	python3 combineS3Files.py --bucket 'liangchun-bucket' --folder 'year2019/$i' --suffix '.mentions.csv' --output 'data/mentions.csv$i' --filesize 1000000000

    # aws s3 cp s3://gdelt-open-data/v2/events/ s3://liangchun-bucket/year2019/$i/ --recursive --exclude "*" --include "2019$i????????.export.csv"
    # aws s3 cp s3://gdelt-open-data/v2/mentions/ s3://liangchun-bucket/year2019/$i/ --recursive --exclude "*" --include "2019$i????????.mentions.csv"
    aws s3 cp http://data.gdeltproject.org/gdeltv2/ s3://liangchun-bucket/year2019/$i/ --recursive --exclude "*" --include "2019$i????????.export.csv"
    aws s3 cp http://data.gdeltproject.org/gdeltv2/ s3://liangchun-bucket/year2019/$i/ --recursive --exclude "*" --include "2019$i????????.mentions.csv"
done