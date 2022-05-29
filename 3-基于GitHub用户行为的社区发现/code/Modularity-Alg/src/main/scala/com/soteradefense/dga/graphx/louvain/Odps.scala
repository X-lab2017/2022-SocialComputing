package com.soteradefense.dga.graphx.louvain

import com.aliyun.odps.TableSchema
import com.aliyun.odps.data.Record

import org.apache.spark.aliyun.odps.OdpsOps
import org.apache.spark.{SparkConf, SparkContext}
//
//ACCESS_ID = 'LTAI5tHDArybZRnXaPS3pdkJ'
//SECRET_ACCESS_KEY = 'lXXLM2U1dB3ExgKquGUwdGb88WHqkN'
//
//ODPS_PROJECT = 'OpenDigger_prod_dev'
//ODPS_ENDPOINT = 'http://service.cn-shanghai.maxcompute.aliyun.com/api'

class Odps {
  def run(sc): Unit = {
    // == Step-1 ==
    val accessKeyId = "LTAI5tHDArybZRnXaPS3pdkJ"
    val accessKeySecret = "lXXLM2U1dB3ExgKquGUwdGb88WHqkN"
    // 以内网地址为例。
    val urls = Seq("http://service.cn-shanghai.maxcompute.aliyun.com/api", "https://dt.cn-shanghai.maxcompute.aliyun.com")
    val odpsOps = OdpsOps(sc, accessKeyId, accessKeySecret, urls(0), urls(1))
    // 下面是一些调用代码。
    // == Step-2 ==
    val project = 'OpenDigger_prod_dev'
    val table = 'ods_github_log'
    val inputData = odpsOps.readTable(project, table, (r: Record, schema: TableSchema) => (r.getString("type"), r.getBigInt("actor_id"), r.getString("member_id"))
    val filtered = inputData.filter(v => ((v._1 == "MemberEvent")&&(v._2 != null)&&(v._3 != null))).map(v=>(v._2, v._3))
    return filtered
    // == Step-3 ==
    ...
  }
  // == Step-2 ==

  }
  // == Step-3 ==
  // 方法定义2
  ｝
