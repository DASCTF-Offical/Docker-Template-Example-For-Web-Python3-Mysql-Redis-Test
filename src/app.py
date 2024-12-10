import json
import redis

from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


@app.route('/')
def index():
    user_id = request.args['id']

    # 初始化数据库连接
    engine = create_engine("mysql+pymysql://test:123456@127.0.0.1/test", encoding="utf-8")

    # 创建session类型
    DBSession = sessionmaker(bind=engine)

    # 创建session对象
    session = DBSession()

    # 执行语句，获取结果
    result = session.execute("select * from users where id = " + user_id)

    # 初始化 redis 连接
    r = redis.Redis(host='127.0.0.1', port=6379, password='root', db=0, decode_responses=True)

    # 设置键值
    r.set('testKey', 'HelloRedis')

    return json.dumps({'result': [dict(row) for row in result], 'redis': r.get('testKey')})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
