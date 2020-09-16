from redis import StrictRedis
import redis

class Redis:
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0):
        self.host = redis_host
        self.port = redis_port
        self.db = redis_db
        self.con = self.connect()

    def connect(self):
        try:
            con = self.con = redis.StrictRedis(
            host=self.host,
            port=self.port,
            db=self.db)
            if con:
                print('Redis is connected : ', con)
                return con
        except Exception as e:
            print(e)
            print("RedisUtil Connection Error")
            con = self.con = None

    def set(self, redis_key, redis_value, exp_s=None, exp_ms=None):
        self.con.set(redis_key, redis_value, exp_s, exp_ms)
        return 'key:value is set in-memory cache'

    def get(self, redis_key):
        # print(redis_key)
        return self.con.get(redis_key)

    def delete(self, *names):
        # print(names)
        self.con.delete(*names)

    def setlist(self,redis_list,redis_value):
        self.con.lpush(redis_list,redis_value)

    def displaylist(self,mylist):
        self.con.ltrim(mylist,0,2)
        return self.con.lrange(mylist,0,-1)