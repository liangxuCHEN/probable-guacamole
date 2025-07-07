# 绑定的ip与端口
bind = "0.0.0.0:8000"

# 工作进程数
workers = 5

# 工作模式
worker_class = 'gevent'

# 最大客户端并发数量
worker_connections = 1000

# 进程文件
pidfile = '/var/run/gunicorn.pid'

# 访问日志和错误日志
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'

# 日志级别
loglevel = 'info'

# 设置守护进程
daemon = False

# 设置超时时间
timeout = 30

# 设置最大请求数
max_requests = 500

# 设置最大请求抖动值
max_requests_jitter = 50

# 设置进程名称
proc_name = 'innrg_gunicorn'
# 设置worker进程的最大内存
limit_request_line = 1024
# 请求头的最大数量
limit_request_fields = 50
# 单个请求头的最大大小
limit_request_field_size = 4095
