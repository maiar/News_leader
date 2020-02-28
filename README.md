# News Leaders by Liangchun Xu

## Table of Contents
1. [Problem](README.md#problem)
1. [Datasets](README.md#datasets)
1. [Data Pipeline](README.md#data-pipeline)
1. [Running Instructions](README.md#running-instructions)
1. [Demo](README.md#demo)
1. [Files in Repo](README.md#files-in-repo)
1. [Engineering Challenge](README.md#engineering-challenge)
1. [Conclusion](README.md#conclusion)
1. [Contact Information](README.md#contact-information)

## Problem

Numerous social events are reported everyday on Internet. To sift through large amount of information, at Insight, I built a tool to quickly identify the top 10 reported news events (News Leaders) in a given time. It can help decision makers to quickly reach the most popular news sources.

## Datasets
The GDELT Event database v2.0 and the GDELT Mentions table, available on GDELT's [official website](http://data.gdeltproject.org/gdeltv2). 

## Data Pipeline

![Pipeline](img/datapipeline.png)

The data pipeline is illustrated above. First the GDELT data is read into Amazon S3. Then Apache Spark reads the data into dataframes and count the number of each news link is distributely computed on 4 cluster nodes. The final resulting dataframe is collected and sent into PostgreSQL for storage. The final result is shown via Dash.

## Running Instructions
* Spin up an EC2 instance (or cluster). 
* Make sure Spark is installed on all the instances.
* Make sure that all the python and system requirements (in requirements.txt) are installed.
* Clone this repo to the master EC2 node. 
* Go to News_leader/web_application/ in your terminal.
* Type "python webapp.py".
* Go to the website that is specified. 
* Enter the information as prompted. 
* Hit Submit. 

## Demo

[Here](https://www.youtube.com/watch?v=UZWLIDdekdg) you can see a video of my application in the works. 

In the first part, you can see an example of data that is stored in an S3 Bucket. Then you see the front end, where the information is inputted. Then the program is run and we return to the S3 Bucket to see that our information is now there. Once we look at it, we see that the columns that were specified have been encrypted. 

Here you can see my [slides](https://bit.ly/2SCd4Nh). 

## Files in Repo 

### datapipeline.py

#### description: 
This file reads the S3 data into spark and computes the citations of each news link. The final result and two raw datasets are written into the PostgreSQL database.    

### webapp.py

#### description:
This is a Dash frontend page, which makes queries and reads data from the PostgreSQL database to visualize the news leaders results various forms.

## Engineering Challenge
Spark performance bottleneck is met when I scaled the data size from single file to daily files. The execution time increases from 28 s to 12 min. The reading of large sets of scattering data files is the cause behind the scene. I solved the problem by combining the raw data files into one before Spark processing. It can significantly improve the performance. 

## Conclusion

News Leader is built to source the most cited news links on the Internet and hopefully answers the questions that where the events come from and help people assess the credibility of these most popular news stories.

## Contact Information
* LinkedIn: [Liangchun Xu](https://www.linkedin.com/in/liangchunxu/)
* Email: maiar@outlook.com
