# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import sys
from operator import add
import pyspark.sql
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import pyspark
from pyspark.sql import Row
from pyspark.sql import DataFrameWriter
import re

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("GFGData")\
        .getOrCreate()
    #mentionFileStr = 's3a://gdelt-open-data/v2/mentions/20150603061500'+'.mentions.csv'
    #eventFileStr = 's3a://gdelt-open-data/v2/events/20150623061500'+'.export.csv'
    #mentionFileStr = 's3a://gdelt-open-data/v2/mentions/20150603??????'+'.mentions.csv'
    #eventFileStr = 's3a://gdelt-open-data/v2/events/20150623??????'+'.export.csv'
    mentionFileStr = 's3a://liangchun-bucket/output/mentions.csv-0'
    eventFileStr = 's3a://liangchun-bucket/output/events.csv-0'
    print(eventFileStr)
    print(mentionFileStr)

    sqlContext = SQLContext(sparkContext=spark.sparkContext, sparkSession=spark)
    mentionDf = sqlContext.read.load(mentionFileStr, format='com.databricks.spark.csv', inferSchema='true')
    eventDf = sqlContext.read.load(eventFileStr, format='com.databricks.spark.csv', inferSchema='true')
    mentionDf = mentionDf.selectExpr('SPLIT(_c0, "\t")[0] AS GlobalEventID', 'SPLIT(_c0, "\t")[1] AS EventTimeDate', 'SPLIT(_c0, "\t")[2] AS MentionTimeDate', 'SPLIT(_c0, "\t")[3] AS MentionType','SPLIT(_c0, "\t")[4] AS MentionSourceName', 'SPLIT(_c0, "\t")[5] AS MentionIdentifier')
    eventDf = eventDf.selectExpr('SPLIT(_c0, "\t")[0] AS GlobalEventID', 'SPLIT(_c0, "\t")[25] AS IsRootEvent', 'SPLIT(_c0, "\t")[40] AS Lat', 'SPLIT(_c0, "\t")[41] AS Long')    

    mentionDf.printSchema()
    eventDf.printSchema()
    citationDf = mentionDf.groupBy("MentionIdentifier").count()
    citationDf.show()

    mentionDf.write \
    .jdbc("jdbc:postgresql://liangchun-database.csbeke3v1jfz.us-east-1.rds.amazonaws.com:5432/newsLeader", "public.mentions", properties={"user": "postgres", "password": "Tianya1990"}, mode = "overwrite") 
   
    eventDf.write \
    .jdbc("jdbc:postgresql://liangchun-database.csbeke3v1jfz.us-east-1.rds.amazonaws.com:5432/newsLeader", "public.events", properties={"user": "postgres", "password": "Tianya1990"}, mode = "overwrite") 

    citationDf.write \
    .jdbc("jdbc:postgresql://liangchun-database.csbeke3v1jfz.us-east-1.rds.amazonaws.com:5432/newsLeader", "public.citations", properties={"user": "postgres", "password": "Tianya1990"}, mode = "overwrite")    

    spark.stop()
