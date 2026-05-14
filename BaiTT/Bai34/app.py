from flask import Flask, request
import redis
from datetime import datetime

app = Flask(__name__)
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
	today = datetime.now().date().isoformat()

	key = f"ua:{today}"

	user_agent = request.headers.get('User-Agent','')
	r.pfadd(key, user_agent)

	count = r.pfcount(key)

	return str(count) + '\n'

if __name__== '__main__':
	app.run()
