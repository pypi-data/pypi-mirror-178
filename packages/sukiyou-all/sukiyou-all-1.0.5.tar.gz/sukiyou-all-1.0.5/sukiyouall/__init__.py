import os

# t_path = '../../../../'
t_path = './'

dir_list = [
	'bin',
	'config',
	'core',
	'interface',
	'lib',
	'log',
	'models',
	'static',
	'test',
]
for x in dir_list:
	try:
		os.mkdir(t_path + x)
	except:
		pass

with open(t_path + 'config/access.ini', 'w', encoding='utf-8') as f:
	f.write(
		r"""[access_token]
issuer = seven
key = seven
expiration_time = 1800"""
	)
	pass
with open(t_path + 'config/blueprint.ini', 'w', encoding='utf-8') as f:
	f.write(
		r"""[blue-print]
; 您不应该注册名为 <upload> 的蓝图
; 您应该避免 python mysql 关键字 如一定要使用 请使用复数形式
;creates = creates
;deletes = deletes
;updates = updates
;searchs = searchs"""
	)
	pass
with open(t_path + 'config/db.ini', 'w', encoding='utf-8') as f:
	f.write(
		r"""[mysql]
user = 
pwd = 
host = 
dbname = """
	)
	pass
with open(t_path + 'config/env.ini', 'w', encoding='utf-8') as f:
	f.write(
		r"""[venv]
; 0 生产
; 1 开发
env = 1
;env = 0"""
	)
	pass
with open(t_path + 'config/err-msg.ini', 'w', encoding='utf-8') as f:
	f.write(
		r"""[error-code]"""
	)
	pass
with open(t_path + 'config/host.ini', 'w', encoding='utf-8') as f:
	f.write(
		r"""[host]
domain = http://www.baidu.com
venv_domain = http://www.baidu.com"""
	)
	pass
with open(t_path + 'config/wx_info.ini', 'w', encoding='utf-8') as f:
	f.write(
		r"""[wxinfo]
APPID =
SECRET ="""
	)
	pass
# core
with open(t_path + 'core/blueprint_imp.py', 'w', encoding='utf-8') as f:
	f.write(
		r"""  """
	)
	pass
# interface
with open(t_path + 'interface/interface_import.py', 'w', encoding='utf-8') as f:
	f.write(
		r"""  """
	)
	pass
#lib
with open(t_path + 'lib/access_token.py', 'w', encoding='utf-8') as f:
	f.write(
		r"""# -*- coding: utf-8 -*-
import jwt
import time
from lib.ini_info import *

issuer, key, expiration_time = get_info()


def create_token(openid):
	d = {
        # 公共声明
        'exp': time.time() + expiration_time,  # (Expiration Time) 此token的过期时间的时间戳
        'iat': time.time(),  # (Issued At) 指明此创建时间的时间戳
        'iss': issuer,  # (Issuer) 指明此token的签发者
        # 私有声明
        'data': {
            'openid': openid,
            'timestamp': time.time(),
        }
    }

    token = jwt.encode(d, key, algorithm='HS256')

    return token


def decode_token(token):
    res = jwt.decode(token, key, issuer=issuer, algorithms=['HS256'])
    return res
  """
	)
	pass
with open(t_path + 'lib/annotation.py', 'w', encoding='utf-8') as f:
	f.write(
		r"""# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from flask import g as sukiyou_global
from lib.access_token import decode_token


def check_token(f):
	@wraps(f)
	def check():
		data = request.get_json()
		token = data.get('token')
		if token is not None:
			try:
				res = decode_token(token)
				sukiyou_global.openid = res.get("openid")
				sukiyou_global.sukiyou_appid = res.get('sukiyou_appid')
				return f()
			except:
				return ['token has expiration']

			pass
		else:
			return ['token has gone']
	return check

  """
	)
	pass
with open(t_path + 'lib/blueprint_conf.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''# -*- coding: utf-8 -*-
from lib.ini_info import blue_print_info

import os

res = blue_print_info()
with open('lib/blueprint_register.py', 'w', encoding='utf-8') as f:
    f.write(f"""
from flask import Flask
from lib.blueprint_info import *

app = Flask(__name__, static_folder="./../static")
# 蓝图注册
    """)
    f.close()

with open('lib/blueprint_info.py', 'w', encoding='utf-8') as f:
    f.write(f"""
from flask import Blueprint
        """)
    f.close()
for x in res:
    with open('lib/blueprint_info.py', 'a', encoding='utf-8') as f:
        f.write(f"""
{x} = Blueprint('{x}', __name__, url_prefix="/{res[x]}")
        """)
        f.close()

    with open('lib/blueprint_register.py', 'a', encoding='utf-8') as f:
        f.write(f"""
app.register_blueprint({x})
    """)
        f.close()
        pass

    pass
'''
	)
	pass
with open(t_path + 'lib/blueprint_upload.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''# -*- coding: utf-8 -*-
from flask import Blueprint, request
from lib.snow_id import *
import os
# from lib.ini_info import upload_host

# host_domain = upload_host()

upload = Blueprint('upload', __name__, url_prefix="/upload")


@upload.route('/', methods=['GET', 'POST'])
def uploads__():
    try:
        worker = IdWorker(1, 4, 0)
        uid = worker.get_id()
        file_obj = request.files['file']
        if file_obj is None:
            return 9001
        filename = file_obj.filename.split('.')
        filename[0] = uid
        filenamet = str(filename[0]) + '.' + filename[1]
        file_type = str(file_obj.headers['Content-Type']).split('/')
        if 'video' in file_type:
            file_obj.save("static/video/" + filenamet)
        else:
            file_obj.save("static/" + filenamet)
        return file_obj.filename
    except Exception as a:
        return "文件上传失败"


@upload.route('/del', methods=['GET', 'POST'])
def del_uploads__():
    url = "/static/1.jpg"
# def del_uploads__(url):
    url_list = url.split('/')
    try:
        # 找到文件名
        for x in url_list:
            if x.find('.') != -1:
                # 删除他
                os.remove(os.getcwd() + "/static/" + x)
        return "文件删除成功"
    except Exception as e:
        return f"文件删除失败 ==> {e}"

    pass
		'''
	)
	pass
with open(t_path + 'lib/config_r.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''# -*- coding: utf-8 -*-
import configparser
import os


class readini:
	def __init__(self, file="db.ini"):
		self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件目录
		self.ConfigPath = os.path.join(self.BASE_DIR, '../config')  # 自己的配置文件路径，根据项目需求，这里是--> 在当前目录下的config下存放目录文件
		self.slat = "IchLiebeWangLanPink"
		self.conf = configparser.ConfigParser()
		self.file_name = file
		self.file_path = os.path.join(self.ConfigPath, self.file_name)
		...

	def readr(self, pal='mysql'):
		"""
		:param pal: sectionName
		:return:
		"""
		self.conf.read(self.file_path, encoding="utf-8")  # python3
		res = self.conf.items(pal)
		t = {}
		for x in res:
			x = list(x)
			p = {x[0]: x[1]}
			t.update(p)
		return t
		'''
	)
	pass
with open(t_path + 'lib/database_conn.py', 'w', encoding='utf-8') as f:
	f.write(
		r"""import datetime
import json

from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from lib.config_r import readini
from lib.ini_info import DB_INFO

db_info = DB_INFO()

engine = create_engine(f"mysql+pymysql://{db_info.get('user')}:{db_info.get('pwd')}"
                       f"@{db_info.get('host')}/{db_info.get('dbname')}?",
                       echo=False,
                       pool_recycle=10,
                       pool_size=10,
                       max_overflow=5,
                       pool_timeout=10,
                       isolation_level="READ UNCOMMITTED"
                       )

SQLALCHEMY_POOL_RECYCLE = 10
SQLALCHEMY_POOL_TIMEOUT = 10

Base = declarative_base()

# 创建session
DbSession = sessionmaker(bind=engine)


# session = DbSession()


class CUdr:

    def __init__(self):
        pass

    @classmethod
    def insert(cls, emps):
        '''
        emps = Store_score(
            store_id=store_id,
            class . column = val
        )
        '''
        session = DbSession()
        try:
            session.add(emps)
            session.commit()
            return True
        except Exception as e:
            print(f"e==>{e} <=")
            session.rollback()
            return False

        finally:
            session.close()

    @classmethod
    def delete_real(cls, filter):
        session = DbSession()
        try:
            res = session.query(cls)
            for x in filter:
                res = res.filter(x)

            res.delete()
            session.commit()
            return True
        except:
            session.rollback()
            return False

        finally:
            session.close()

    @classmethod
    def delete(cls, filter):
        session = DbSession()
        try:
            res = session.query(cls)
            for x in filter:
                res = res.filter(x)
            update = {
                'is_use': 0
            }
            res.update(update)
            session.commit()
            return True
        except:
            session.rollback()
            return False

        finally:
            session.close()

    @classmethod
    def update(cls, filter, update: dict):
        '''
        :param filter: 查询条件
        :param update: 更改内容
        :return:
        :ex.
                update = {
                    'nick_name': nick_name,
                    'phone': phone
                }
                filter = {User.id == id}
        '''
        session = DbSession()
        try:
            res = session.query(cls)
            for x in filter:
                res = res.filter(x)
            # res = res.filter(filter)
            res.update(update)
            session.commit()
            return True
        except:
            session.rollback()
            return False

        finally:
            session.close()

    @classmethod
    def __other_info(cls, session):
        res = session.query(cls).count()
        return res

    @classmethod
    def fetch_all(cls, limit=False, group=False, order: tuple = False, filter: dict = False):

        session = DbSession()
        last_page = 'no limit'

        res = session.query(cls)
        if filter:
            for x in filter:
                res = res.filter(x)
        if group:
            res = res.group_by(group)
        if order:
            if order[1]:
                res = res.order_by(order[0].desc())
            else:
                res = res.order_by(order[0])
        if limit:
            start = (limit[0] - 1) * limit[1]
            stop = limit[0] * limit[1]
            try:
                res2 = res.slice(start, stop).all()
            except:
                session.rollback()
                res2 = res.slice(start, stop).all()
            res_len = len(res2)
            last_page = False
            if res_len < limit[1]:
                last_page = True
            res = res.slice(start, stop)
        try:
            res = res.all()
        except:
            session.rollback()
            res = res.all()
        session.flush()
        a = []
        for x in res:
            x = cls.to_dict(x)
            a.append(x)
        count = cls.__other_info(session)
        result = {
            "list": a,
            "list_length": len(res),
            "total_count": count,
            "lastPage": last_page
        }
        session.close()
        return result

    @classmethod
    def fetch_one(cls, limit=False, group=False, order: tuple = False, filter=False):

        session = DbSession()
        res = session.query(cls)
        if filter:
            for x in filter:
                res = res.filter(x)
        try:
            res = res.first()
        except:
            session.rollback()
            res = res.first()
        session.flush()
        result = {
            "list": cls.to_dict(res),
        }
        res = cls.to_dict(res)
        session.close()
        return res

    def __repr__(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]

        return json.dumps(fields, cls=DateEncoder, ensure_ascii=False)

    @classmethod
    def to_dict(cls, obj):
        if obj is None:
            return None
        d = dict()
        for c in cls.__table__.columns:
            v = getattr(obj, c.name)
            if c.name == "create_time" or c.name == 'update_time':
                v = v.strftime("%Y-%m-%d %H:%M:%S")
            d[c.name] = v
        return d


# 处理json格式化时 时间问题
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

		"""
	)
	pass
with open(t_path + 'lib/errorlog.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''import os
import time


class errorlogs:
	def __init__(self):
		self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件目录
		self.ConfigPath = os.path.join(self.BASE_DIR, '../log')  # 自己的配置文件路径，根据项目需求，这里是--> 在当前目录下的config下存放目录文件
		self.file_name = "app_err_log.log"
		self.file_path = os.path.join(self.ConfigPath, self.file_name)

	def writeLog(self, path, method, text, status):
		writetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		file = open(self.file_path, 'a+', encoding='utf8')
		str='[ time=> (' + writetime + ') ] - [ method=>' + method + ' ] - [ path=>' + path + ' ] - [ error_code=> ' + status + ' ] - [ error_message=> { ' + text + ' } ]  \n'
		file.write(str)
		file.close()

		
		'''
	)
	pass
with open(t_path + 'lib/exceptions.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''class InvalidSystemClock(Exception):
    """
    时钟回拨异常
    """
    pass

		'''
	)
	pass
with open(t_path + 'lib/ini_info.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''from lib.config_r import readini

env = readini('env.ini').readr('venv')['env']
if env == 0:
    # product
    venv = False
else:
    # development
    venv = True


def blue_print_info():
    return readini('blueprint.ini').readr('blue-print')


def DB_INFO():
    return readini().readr()


def get_info():
    token_info = readini('access.ini').readr('access_token')
    issuer = token_info['issuer']
    key = token_info['key']
    expiration_time = int(token_info['expiration_time'])

    return issuer, key, expiration_time


def upload_host():
    res = readini('host.ini').readr('access_token')
    if venv:
        host_domain = res['venv_domain']
    else:
        host_domain = res['domain']
    return host_domain

		'''
	)
	pass
with open(t_path + 'lib/main_app.py', 'w', encoding='utf-8') as f:
	f.write(
		r"""import json

from flask_cors import *
from flask import g
from lib.errorlog import errorlogs
from lib.access_token import create_token

from lib.annotation import *

#  init server system


# 蓝图
try:
    # 未创建蓝图时 报错时正常的
    from lib.blueprint_conf import *
    from lib.blueprint_info import *
    from lib.blueprint_register import *
except:
    print("当前工作区无蓝图")
    pass

# 文件上传及删除
from lib.blueprint_upload import *

# 注册文件系统
app.register_blueprint(upload)

CORS(app, supports_credentials=True)  # 设置跨域

from core.blueprint_imp import *

# init log system
__log__ = errorlogs()


@app.route('/get-token', methods=['POST'])
def get_token():
    '''
    :param : openid 用户身份标识
    :param : my_appid 本程序的唯一id 随意生成
    :return:
    '''
    data = request.get_json()
    openid = data.get('openid')
    sukiyou_appid = data.get('my_appid')
    return [create_token({
        "openid": openid,
        "sukiyou_appid": sukiyou_appid
    })]


@app.route('/', methods=['POST', 'GET'])
def testfalknsdfjnsf():
    sukiyou_global.message = "success"
    return ["恭喜,安装成功"]


@app.before_request
def __before_requests___():
    pass


@app.after_request
# @check_error_msg
def __after__(response):
    # ------------------- 定义返回值 -----------------------------------------
    try:
        if type(eval(response.data)) is list or type(eval(response.data)) is dict:
            msg = "success"
            if g.get('message'):
                msg = g.get('message')
            response.data = json.dumps({"message": msg, "code": '0', 'data': eval(response.data)}, ensure_ascii=False)
            error_code = 200
        else:
            msg = response.data.decode('utf-8')
            response.data = json.dumps(
                {"message": "<route>[ " + request.path + " ]<error>[ " + response.data.decode('utf-8') + " ]",
                 "code": '0',
                 'data': False}, ensure_ascii=False)
            error_code = 500
    except:
        try:
            msg = response.data.decode('utf-8')
            response.data = json.dumps(
                {"message": "<route>[ " + request.path + " ]<error>[ " + response.data.decode('utf-8') + " ]",
                 "code": '0',
                 'data': False}, ensure_ascii=False)
            error_code = 500
        except:
            msg = "未知 image?"
            error_code = 7
            pass
    # -------------------- 写日志 ---------------------------------------------
    __log__.writeLog(request.path, request.method, str(msg), str(error_code))
    return response
"""
	)
	pass
with open(t_path + 'lib/public.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''import hashlib
import time
import json

import requests


def get_loca_time():
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def su_sha256(data):
	hashs = hashlib.sha256()
	hashs.update(data.encode('utf-8'))
	return hashs.hexdigest()


def decode_aes(e):
	url = "https://h5.rubyonly.cn/php_aes/index.php"
	# url = "http://localhost/aes/aes.php"
	data = {
		'data': e['encryptedData'],
		'key': e['key'],
		'iv': e['iv'],
		'type': 'de',
	}
	res = requests.post(url, data)
	return json.loads(res.text)


		'''
	)
	pass
with open(t_path + 'lib/snow_id.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''# Twitter's Snowflake algorithm implementation which is used to generate distributed IDs.
# https://github.com/twitter-archive/snowflake/blob/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala

import time
import logging

from lib.exceptions import InvalidSystemClock

# 64位ID的划分
WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12

# 最大取值计算
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# 移位偏移计算
WOKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# Twitter元年时间戳
TWEPOCH = 1288834974657

logger = logging.getLogger('flask.app')


class IdWorker(object):
    """
    用于生成IDs
    """

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        初始化
        :param datacenter_id: 数据中心（机器区域）ID
        :param worker_id: 机器ID
        :param sequence: 其实序号
        """
        # sanity check
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id值越界')

        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id值越界')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1  # 上次计算的时间戳

    def _gen_timestamp(self):
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def get_id(self):
        """
        获取新ID
        :return:
        """
        timestamp = self._gen_timestamp()

        # 时钟回拨
        if timestamp < self.last_timestamp:
            logging.error('clock is moving backwards. Rejecting requests until {}'.format(self.last_timestamp))
            raise InvalidSystemClock

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << DATACENTER_ID_SHIFT) | \
                 (self.worker_id << WOKER_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp

# if __name__ == '__main__':
#     worker = IdWorker(1, 2, 0)
#     # print(worker.get_id())

		'''
	)
	pass
with open(t_path + 'lib/wx.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''import json

import requests

from lib.config_r import readini
from lib.public import decode_aes


class wx_inc:
	def __init__(self):
		try:
			self.wxinfo = readini('wx_info.ini').readr('wxinfo')
		except:
			self.wxinfo = False
		if not self.wxinfo:
			return

	def auth_code2session(self, code, data={}):
		url = f"https://api.weixin.qq.com/sns/jscode2session?" \
			  f"appid={self.wxinfo.get('APPID')}&" \
			  f"secret={self.wxinfo.get('SECRET')}&" \
			  f"js_code={code}&" \
			  f"grant_type=authorization_code"
		response = requests.get(url=url)
		response = json.loads(response.text)
		if response['errcode'] == 0:
			try:
				session_key = response['session_key']
				encryptedData = data['encryptedData']
				iv = data['iv']
				encryptedData_info = decode_aes({'encryptedData': encryptedData, 'key': session_key, 'iv': iv})
				phone = encryptedData_info['phoneNumber']
			except:
				phone = '获取失败'
				pass
			response['phone'] = phone
			return response

		
		'''
	)
	pass
with open(t_path + 'models/create_model.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''import os

from lib.ini_info import DB_INFO

db_info = DB_INFO()

table_list = [
]
for x in table_list:
    print(x + '\r')
    command = "sqlacodegen  --outfile " + x + ".py --table " + x + f" mysql+pymysql://{db_info.get('user')}:{db_info.get('pwd')}@{db_info.get('host')}/{db_info.get('dbname')}?charset=utf8"
    os.system(command)

		'''
	)
	pass
with open(t_path + 'models/ex_import.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''from lib.database_conn import *
from lib.public import *
from sqlalchemy import *
from sqlalchemy.dialects.mysql import *

import hashlib

		'''
	)
	pass
with open(t_path + 'app.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''from lib.main_app import app, g, __log__
# main_app 内包含一个 '/' 路由用于测试服务是否启动成功
#				一个 after_request方法, 重新格式化返回值及写流水日志
#
# -----------------------------------------------
# -----------------------------------------------
app.run(port=12369, host='0.0.0.0', debug=True)

		'''
	)
	pass

# 空目录
with open(t_path + 'log/sukiyou.sukiyou', 'w', encoding='utf-8') as f:
	f.write(
		r'''
test write
		'''
	)
	pass