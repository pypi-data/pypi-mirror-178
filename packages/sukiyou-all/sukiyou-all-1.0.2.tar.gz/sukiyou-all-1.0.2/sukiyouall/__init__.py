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
	'test',
]
for x in dir_list:
	try:
		os.mkdir(t_path + x)
	except:
		pass

with open(t_path + 'config/db.ini', 'w', encoding='utf-8') as f:
	f.write(
		r"""
[mysql]
		"""
	)
	pass
with open(t_path + 'config/access.ini', 'w', encoding='utf-8') as f:
	f.write(
		r"""
[access_token]
		"""
	)
	pass
with open(t_path + 'config/blueprint.ini', 'w', encoding='utf-8') as f:
	f.write(
		r"""
[blue-print]
		"""
	)
	pass
with open(t_path + 'config/err-msg.ini', 'w', encoding='utf-8') as f:
	f.write(
		r"""
[error-code]
		"""
	)
	pass
with open(t_path + 'config/wx_info.ini', 'w', encoding='utf-8') as f:
	f.write(
		r"""
[wxinfo]
		"""
	)
	pass
with open(t_path + 'readme.md', 'w', encoding='utf-8') as f:
	f.write(
		r"""
```python

# ini 配置文件内 节点名称不可更改
# 已存在变量不可重命名
```
		"""
	)
	pass

with open(t_path + 'core/errorlog.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''
import os
import time


class errorlogs:
	def __init__(self):
		self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件目录
		self.ConfigPath = os.path.join(self.BASE_DIR, '../log')  # 自己的配置文件路径，根据项目需求，这里是--> 在当前目录下的config下存放目录文件
		self.file_name = "app_err_log.txt"
		self.file_path = os.path.join(self.ConfigPath, self.file_name)

	def writeLog(self, path, method, text, status):
		writetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		file = open(self.file_path, 'a+', encoding='utf8')
		str='[ time=> (' + writetime + ') ] - [ method=>' + method + ' ] - [ path=>' + path + ' ] - [ error_code=> ' + status + ' ] - [ error_message=> { ' + text + ' } ]  \n'
		file.write(str)
		file.close()

		'''
	)

with open(t_path + 'interface/interface_import.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''
#
		'''
	)

with open(t_path + 'lib/config_r.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''
# -*- coding: utf-8 -*-
# :PROJECT_NAME : flask-forder
# :PRODUCT_NAME : PyCharm
# @Desc ====================================================
# :Author : SEVEN
# :Path :
# :File : read.py
# :Time : 2022-02-24 18:02
# @Desc ====================================================
# :Param : {name : pal , type : string ,paraphrase : sectionName}
# :Return : [dict]
# @signature : [165eba193235128754c4ccf4e17afa69c54a6b76199bc3cc98d92e18e88a6c6e]
# Copyright belongs to the author.
# Commercial reprint please contact the author for authorization, non-commercial reprint please indicate the source.


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


# if __name__ == '__main__':
# 	res = readini('err-msg.ini').readr('error-code').get('success')
# 	print(res)

		'''
	)

with open(t_path + 'lib/database_conn.py', 'w', encoding='utf-8') as f:
	f.write(
r"""
import datetime
import json

from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from lib.config_r import readini

DB_INFO = readini().readr()
engine = create_engine(f"mysql+pymysql://{DB_INFO.get('user')}:{DB_INFO.get('pwd')}"
					   f"@{DB_INFO.get('host')}/{DB_INFO.get('dbname')}?",
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
with open(t_path + 'lib/main_app.py', 'w', encoding='utf-8') as f:
	f.write(
r"""
from lib.ini_info import *
import base64
import json
import os
import uuid

from flask import Flask, render_template, url_for, Blueprint
from flask_cors import *
from werkzeug.utils import secure_filename, redirect
from flask import g
from core.errorlog import errorlogs
from lib.access_token import create_token

from lib.annotation import *
from lib.config_r import readini

#  init server system
app = Flask(__name__)

# 蓝图
try:
	from lib.blueprint_conf import *
	from lib.blueprint_info import *
except:
	print("当前工作区无蓝图")
	pass

CORS(app, supports_credentials=True)  # 设置跨域

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
			response.data = json.dumps({"message": msg, "code": '0', 'data': eval(response.data)})
			error_code = 200
		else:
			msg = response.data.decode('utf-8')
			response.data = json.dumps(
				{"message": "<route>[ " + request.path + " ]<error>[ " + response.data.decode('utf-8') + " ]",
				 "code": '0',
				 'data': False})
			error_code = 500
	except:
		msg = response.data.decode('utf-8')
		response.data = json.dumps(
			{"message": "<route>[ " + request.path + " ]<error>[ " + response.data.decode('utf-8') + " ]", "code": '0',
			 'data': False})
		error_code = 500
	# -------------------- 写日志 ---------------------------------------------
	__log__.writeLog(request.path, request.method, str(msg), str(error_code))
	return response


"""
	)
with open(t_path + 'lib/public.py', 'w', encoding='utf-8') as f:
	f.write(
r"""
import hashlib
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

"""
	)
with open(t_path + 'log/sukiyou.sukiyou', 'w', encoding='utf-8') as f:
	f.write(
		r'''
#
		'''
	)
with open(t_path + 'models/create_model.py', 'w', encoding='utf-8') as f:
	f.write(
r"""
import os

table_list = [
]
for x in table_list:
	print(x + '\r')
	command = "sqlacodegen  --outfile " + x + ".py --table " + x + " mysql+pymysql://seven_pyp_conf:GG6L2eEJmWm6c42m@222.186.150.48:3306/seven_pyp_conf?charset=utf8"
	os.system(command)

"""
	)
with open(t_path + 'models/ex_import.py', 'w', encoding='utf-8') as f:
	f.write(
r"""
from lib.database_conn import *
from lib.public import *
from sqlalchemy import *
from sqlalchemy.dialects.mysql import *

import hashlib
"""
	)

with open(t_path + 'app.py', 'w', encoding='utf-8') as f:
	f.write(
r"""
from lib.main_app import app, g, __log__
# main_app 内包含一个 '/' 路由用于测试服务是否启动成功
#				一个 after_request方法, 重新格式化返回值及写流水日志
#
# -----------------------------------------------
# -----------------------------------------------
app.run(port=12369, host='0.0.0.0', debug=True)
"""
	)

with open(t_path+'lib/wx.py','w',encode='utf-8')as f:
	f.write(
		r"""
import json

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
			# openid = response['openid']
			# session_key = response['session_key']
			# unionid = response['unionid']
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

		"""
	)

with open(t_path+'lib/wx.py','w',encode='utf-8')as f:
	f.write(
r"""
import datetime
import time

import jwt

from lib.config_r import readini

issuer = readini('access.ini').readr('access_token')
key = readini('access.ini').readr('access_token')


def create_token(data: dict):
	d = {
		# 公共声明
		'exp': datetime.datetime.now() + datetime.timedelta(days=1),  # (Expiration Time) 此token的过期时间的时间戳
		'iat': datetime.datetime.now(),  # (Issued At) 指明此创建时间的时间戳
		'iss': issuer,  # (Issuer) 指明此token的签发者
		# 私有声明
		'data': data
	}

	token = jwt.encode(d, key, algorithm='HS256')

	return token


def decode_token(token):
	res = jwt.decode(token, key, issuer=issuer, algorithms=['HS256'])
	return res

"""
	)

with open('lib/blueprint_conf.py', 'a', encoding='utf-8') as f:
	f.write(
r'''
from flask import Blueprint

from lib.ini_info import blue_print_info

import os

res = blue_print_info()
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
		pass

	pass
# p = Blueprint('' + x, __name__, url_prefix="/" + x)


'''
)
with open('lib/ini_info.py', 'a', encoding='utf-8') as f:
	f.write(
r'''
from lib.config_r import readini


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


'''
)
with open('lib/annotation.py', 'a', encoding='utf-8') as f:
	f.write(
r'''
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

'''
)
