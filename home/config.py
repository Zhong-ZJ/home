#coding=utf-8
import os

# Application配置参数
settings = dict(                                        	                           # setting环境配置
        template_path=os.path.join(os.path.dirname(__file__), "templates"),            # 模板文件
        static_path=os.path.join(os.path.dirname(__file__),  "static"),                # 静态文件
        debug=True,
        cookie_secret='aaaa',                               	# 设置cookie密钥
        login_url='/login',                                 	# @authenticated验证不通过直接跳转定义路由
        xsrf_cookies=True,                                  	# 开启xsrf功能

        # pycket的配置信息
        pycket={
            'engine': 'redis',                              	# 设置存储器类型
            'storage': {                                    	# 储存信息
                'host': 'localhost',                        	# 主机
                'port': 6379,                               	# 端口号
                'db_sessions': 5,                           	# 多少号数据库
                'db_notifications': 11,                     	#
                'max_connections': 2 ** 31,                 	# 最大连接
            },
            'cookies': {                                    	# 设置cookie过期时间
                'expires_days': 30,
                'max_age': 5000,
            },
        },
    )




# Redis配置参数
# redis_options = dict(
#     host="127.0.0.1",
#     port=6379
# )



# 日志配置
log_path = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"