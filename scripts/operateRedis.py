import redis

conn = redis.Redis(host='47.97.68.75', password='liu010203040506', port='6379')
result = conn.get('+861829656164')
print(conn.keys())
