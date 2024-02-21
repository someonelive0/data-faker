# -*- coding: utf-8 -*-
# 产生模拟表和模拟字段，并产生模拟数据，进而生产SQL

from mimesis.schema import Schema
import random, time, sys, logging, argparse
from datetime import datetime
import uvicorn
from fastapi import FastAPI

# 注意运行的PWD目录
import sys
sys.path.append(".")
sys.path.append("..")
from fake_data import version, tablename_faker, field_faker, mksql


logger = logging.getLogger('faker_api')
ARG_TABLE_NUMBER = 2
ARG_ITEM_MIN = 20
ARG_ITEM_MAX = 100
ARG_DB = 'mysql'
ARG_INSERT_BENTCH = 40


def init():
    logger.setLevel(logging.DEBUG)
    formator = logging.Formatter(fmt="%(asctime)s [ %(filename)s ]  %(lineno)d行 | [ %(levelname)s ] | [%(message)s]", datefmt="%Y/%m/%d/%X")
    sh = logging.StreamHandler()
    fh = logging.FileHandler("faker_api.log", encoding="utf-8")
    sh.setFormatter(formator)
    fh.setFormatter(formator)
    logger.addHandler(sh)
    logger.addHandler(fh)

def mk_app():
    app = FastAPI(
        docs_url=None, # Disable docs (Swagger UI)
        redoc_url=None, # Disable redoc
    )
    fields_lambda = field_faker.mkfields_lambda()

    @app.get("/")
    def home():
        return {"message": "please use any word to fake data"}

    # param_path 可以是任意字符
    @app.get("/{param_path:path}")
    def anyword(param_path: str):
        logger.debug('request path: %s' % param_path)
        # 生成数据
        # testData = fields_lambda.create(iterations=2)
        schema = Schema(schema=fields_lambda, iterations=random.randint(2, 11))
        items = schema.create()
        return items
    
    return app


# 主函数，用 uvicorn 启动 fastapi 应用
if __name__ == '__main__':
    init()
    app = mk_app()
    uvicorn.run(app=app)
