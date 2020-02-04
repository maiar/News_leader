# censed to the Apache Software Foundation (ASF) under one or more
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

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("GFGData")\
        .getOrCreate()

    sqlContext = SQLContext(sparkContext=spark.sparkContext, sparkSession=spark)
    t1 = sqlContext.read.load('s3a://liangchun-bucket/20150603061500.mentions.csv', format='com.databricks.spark.csv', inferSchema='true')
    t2 = sqlContext.read.load('s3a://liangchun-bucket/20150623061500.export.csv', format='com.databricks.spark.csv', inferSchema='true')
    t1 = t1.selectExpr('SPLIT(_c0, "\t")[0] AS GlobalEventID', 'SPLIT(_c0, "\t")[1] AS EventTimeDate', 'SPLIT(_c0, "\t")[2] AS MentionTimeDate', 'SPLIT(_c0, "\t")[3] AS MentionType','SPLIT(_c0, "\t")[4] AS MentionSourceName', 'SPLIT(_c0, "\t")[5] AS MentionIdentifier')
    links = t1.select("MentionIdentifier")
    links.show()

    linkRdd = links.rdd
    linkRdd.take(3)
    counts = linkRdd.map(lambda x: (x, 1)).reduceByKey(add)
    output = counts.collect()

    #for (word, count) in output:
    #    print("%s: %i" % (word, count))
    print(output)

    #field1 = StructType([StructField("Links", StringType())])
    #field2 = StructType([StructField("Total", IntegerType())])
    linkName = [i[0] for i in output]
    citeNum = [i[1] for i in output]
    R1 = Row('ID', 'MentionIdentifier')
    R2 = Row('ID', 'NumofCitation')
    linkDf = spark.createDataFrame([R1(i, x) for i, x in enumerate(linkName)])
    citeDf = spark.createDataFrame([R2(i, x) for i, x in enumerate(citeNum)])
    #linkDf = spark.createDataFrame(linkName, schema=field1)
    #citeDf = spark.createDataFrame(citeNum, IntegerType())
    linkDf.show()
    citeDf.show()
    #t1.show()
    #t2.show()
    #df.show()
    #df.take(2)
    #linkRankDf = linkDf.join(citeDf,"outer")
    #linkRankDf.show()
    tl = linkDf.alias('tl')
    tc = citeDf.alias('tc')
    innerjoin = tl.join(tc,tl.ID == tc.ID)
    innerjoin.show()
    spark.stop()