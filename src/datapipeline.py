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
from functools import reduce

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("GFGData")\
        .getOrCreate()
    #mentionFileStr = 's3a://gdelt-open-data/v2/mentions/20150603061500'+'.mentions.csv'
    #eventFileStr = 's3a://gdelt-open-data/v2/events/20150623061500'+'.export.csv'

    #mentionFileStr = 's3a://liangchun-bucket/data19/mentions01-0.csv'
    #eventFileStr = 's3a://liangchun-bucket/data19/events01-0.csv'
   
    mentionFileStr = 's3a://liangchun-bucket/data19/mentions.csv'
    eventFileStr = 's3a://liangchun-bucket/data19/events.csv'
    print(eventFileStr)
    print(mentionFileStr)

    sqlContext = SQLContext(sparkContext=spark.sparkContext, sparkSession=spark)
    mentionDf = sqlContext.read.load(mentionFileStr, sep="\t", format='com.databricks.spark.csv', inferSchema='true').withColumnRenamed("_c0","GlobalEventID").withColumnRenamed("_c1","EventDateTime").withColumnRenamed("_c2","MentionDateTime").withColumnRenamed("_c3","MentionType").withColumnRenamed("_c4","DomainName").withColumnRenamed("_c5","Url").drop("_c6").drop("_c7").drop("_c8").drop("_c9").drop("_c10").drop("_c11").drop("_c12").drop("_c13").drop("_c14").drop("_c15")

    eventDf = sqlContext.read.load(eventFileStr, sep="\t", format='com.databricks.spark.csv', inferSchema='true')
    
    eventDf = eventDf.select([c for c in eventDf.columns if c in {'_c0','_c1','_c25','_c56','_c57','_c60'}]).withColumnRenamed("_c0","GlobalEventID").withColumnRenamed("_c25","IsRootEvent").withColumnRenamed("_c56","Latitude").withColumnRenamed("_c57","Longitude").withColumnRenamed("_c60","SourceUrl").withColumnRenamed("_c1", "EventDateTime")

    mentionDf.show()
    mentionDf.printSchema()
    eventDf.printSchema()
    eventDf.show()   

    reportedDf = mentionDf.groupBy("GlobalEventID").count().withColumnRenamed("count","ArticleCounts")

    ta = eventDf.alias('ta')
    ta.show()
    tb = reportedDf.alias('tb');
    reportedDf = ta.join(tb, ["GlobalEventID"])
    reportedDf.show()

    # write the news ranking table into the postgresql
    reportedDf.write \
    .jdbc("jdbc:postgresql://liangchun-database.csbeke3v1jfz.us-east-1.rds.amazonaws.com:5432/newsLeader", "public.newsBase", properties={"user": "postgres", "password": "Tianya1990"}, mode = "overwrite")    

    spark.stop()
