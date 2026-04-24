from flask import Flask, request
import redis
from datetime import datetime

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/')
def count_ua():
	#lay user agent tu header cua request
	ua = request.headers.get('User-Agent', 'Unkown')
	#tao key theo ngay
	today = datetime.now().strftime('%Y-%m-%d')
	key = f"ua:unique:{today}"
	#dung thuat toan hyperlog
	r.pfadd(key, ua)
	count = r.pfcount(key)
	return f"Hom nay co {count} Uset-Agent truy cap.\n"
if __name__ '__main__'
	app.run(host='0.0.0.0', port=8080)

