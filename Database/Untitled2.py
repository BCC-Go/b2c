#!/usr/bin/env python
# coding: utf-8

# In[7]:


import sklearn
import random
import pandas as pd
import numpy as np
# Pyspark Library #
# SQ
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.functions import mean, col, split, regexp_extract, when, lit
# ML
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler, IndexToString
from pyspark.ml.feature import QuantileDiscretizer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.recommendation import ALS
#Make spark session
spark = SparkSession.builder.config( "spark.jars","/b2c/mysql-connector-java-8.0.27.jar")     .master("local").appName("ml_reco").getOrCreate()
#Load data
buylist = spark.read.format("jdbc").option("url","jdbc:mysql://b2cdb.chy6lfqzk3p1.ap-northeast-2.rds.amazonaws.com:3306/b2c")    .option("driver", "com.mysql.cj.jdbc.Driver").option("dbtable", "buylist")     .option("user", "admin").option("password", "SMoEcEXZ6PZUUiqDv5w9").load()
product = spark.read.format("jdbc").option("url","jdbc:mysql://b2cdb.chy6lfqzk3p1.ap-northeast-2.rds.amazonaws.com:3306/b2c")    .option("driver", "com.mysql.cj.jdbc.Driver").option("dbtable", "product")     .option("user", "admin").option("password", "SMoEcEXZ6PZUUiqDv5w9").load()
category_small = spark.read.format("jdbc").option("url","jdbc:mysql://b2cdb.chy6lfqzk3p1.ap-northeast-2.rds.amazonaws.com:3306/b2c")    .option("driver", "com.mysql.cj.jdbc.Driver").option("dbtable", "category_small")     .option("user", "admin").option("password", "SMoEcEXZ6PZUUiqDv5w9").load()
user_recommand = spark.read.format("jdbc").option("url","jdbc:mysql://b2cdb.chy6lfqzk3p1.ap-northeast-2.rds.amazonaws.com:3306/b2c")    .option("driver", "com.mysql.cj.jdbc.Driver").option("dbtable", "user_recommand")     .option("user", "admin").option("password", "SMoEcEXZ6PZUUiqDv5w9").load()
cart = spark.read.format("jdbc").option("url","jdbc:mysql://b2cdb.chy6lfqzk3p1.ap-northeast-2.rds.amazonaws.com:3306/b2c")    .option("driver", "com.mysql.cj.jdbc.Driver").option("dbtable", "cart")     .option("user", "admin").option("password", "SMoEcEXZ6PZUUiqDv5w9").load()
like = spark.read.format("jdbc").option("url","jdbc:mysql://b2cdb.chy6lfqzk3p1.ap-northeast-2.rds.amazonaws.com:3306/b2c")    .option("driver", "com.mysql.cj.jdbc.Driver").option("dbtable", "b2c.like")     .option("user", "admin").option("password", "SMoEcEXZ6PZUUiqDv5w9").load()

# #Extract a specific ratio for each data
# buylist = buylist.sample(withReplacement=False,fraction=0.3)
# cart = cart.sample(withReplacement=False,fraction=1.0)
# like = like.sample(withReplacement=False,fraction=0.8)

#Remove unnecessary values (required value : user_id, product_id, category_(small, mid)_id, avg_star)
buylist = buylist.drop('buy_date','id','count')
product = product.drop('regist_time','price','brand','image')
category_small = category_small.drop('name')

#Rename for union command
product = product.withColumnRenamed('id','product_id')
category_small = category_small.withColumnRenamed('id','category_small_id')

#Merge data
df = cart.unionByName(like,allowMissingColumns=True)
df = df.unionByName(buylist,allowMissingColumns=True)


##
inner_df = df.join(product, on = ["product_id"],how='left').sort("product_id")
stringIndexer = StringIndexer(inputCol='name', outputCol='name_new')

model = stringIndexer.fit(inner_df)
indexed = model.transform(inner_df)

train, test = indexed.randomSplit([0.75, 0.25])
rec = ALS(maxIter=10, regParam=0.01, userCol='user_id', itemCol='name_new',
        ratingCol='avg_star', nonnegative=True, coldStartStrategy='drop')
rec_model = rec.fit(train)

unique_product = indexed.select("name_new").distinct()


# In[13]:


def ml_recom(user_id, n):
    unique_product = load_data()
    a = unique_product.alias('a')
    bought = indexed.filter(indexed['user_id'] == user_id).select('name_new')
    b = bought.alias('b')
    total = a.join(b, a['name_new'] == b['name_new'], how='left')
    not_bought = total.where(col('b.name_new').isNull()).select('a.name_new').distinct()
    not_bought = not_bought.withColumn('user_id', lit(int(user_id)))
    recommender = rec_model.transform(not_bought).orderBy('prediction', ascending=False).limit(n)
    product_id = IndexToString(inputCol='name_new', outputCol='name', labels=model.labels)
    recommendation = product_id.transform(recommender)
    answer = recommendation.join(indexed.drop('user_id'), on = ["name_new"],how='left').sort("product_id")
    return answer.select('user_id','product_id').show()

ml_recom(1,4)