for i in 02 03 04
do
	python3 combineS3Files.py --bucket 'liangchun-bucket' --folder "year2019/$i" --suffix '.export.csv' --output "data19/events$i.csv" --filesize 100000000000
	python3 combineS3Files.py --bucket 'liangchun-bucket' --folder "year2019/$i" --suffix '.mentions.csv' --output "data19/mentions$i.csv" --filesize 100000000000
done