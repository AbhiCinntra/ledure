import multiprocessing

bind = "103.107.67.160:8002"  # Specify the host and port
workers = multiprocessing.cpu_count() * 2  # Adjust the number of workers
timeout = 60
