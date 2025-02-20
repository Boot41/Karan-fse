import multiprocessing

# Gunicorn config variables
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
worker_connections = 1000

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# SSL Configuration
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Process naming
proc_name = "ai_investment_platform"

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# Server hooks
def on_starting(server):
    pass

def on_reload(server):
    pass

def on_exit(server):
    pass
