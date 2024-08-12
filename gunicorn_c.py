import os
#accesslog = './gunicorn.log'
#errorlog = './gunicorn.err.log'
if os.path.exists(accesslog): os.remove(accesslog)
if os.path.exists(errorlog):  os.remove(errorlog)
bind = "127.0.0.1:11451"
workers = 4
worker_class = "gevent"
worker_connections = 2000
timeout = 30
backlog = 2048
max_requests = 1000
limit_request_line = 8182
reload = False
loglevel = 'debug'