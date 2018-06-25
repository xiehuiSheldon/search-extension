# -*- coding:UTF-8 -*-
import pymysql
def get_text():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='chrome_ext',
        charset='utf8')
    cur = conn.cursor()
    # 查询
    sql = """
	SELECT code_id, name, short_intro,
	 json_extract(detail_info, '$.detail_introduce'),
	 json_extract(detail_info, '$.type_name')
	 FROM extensions
	"""
    cur.execute(sql)
    # fetchall返回一个二维元组，每一行是一条数据，一行中的每一列是查询的每个字段
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


import sys,os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, STORED

from jieba.analyse import ChineseAnalyzer


analyzer = ChineseAnalyzer()

schema = Schema(code_id=STORED,
                name=TEXT(stored=True, analyzer=analyzer),
				short_intro=TEXT(stored=True, analyzer=analyzer),
				detail_introduce=TEXT(stored=True, analyzer=analyzer),
				type_name=STORED)

if not os.path.exists("index"):
    os.mkdir("index")

ix = create_in("index", schema) # for create new index
#ix = open_dir("index") # for read only
writer = ix.writer()

res = get_text()
for line in res:
	writer.add_document(
		code_id=line[0],
		name=line[1],
		short_intro=line[2],
		detail_introduce=line[3],
		type_name=line[4]
	)
writer.commit()