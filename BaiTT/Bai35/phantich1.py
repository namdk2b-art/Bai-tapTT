import os
import time
from datetime import datetime, timedelta
from collections import Counter

LOG_FILE = '/var/log/nghttp2/access.log'
CHUNK_SIZE = 64 * 1024

def analyze_last_minute():
	if not os.path.exists(LOG_FILE):
		print(f"Loi : Ko tim thay file {LOG_FILE}")
		return
	#xac dinh moc thoi gian
	now = datetime.now()
	target_time = now - timedelta(minutes=1)
	
	protocols = Counter()
	ciphers = Counter()
	total_count = 0

	with open(LOG_FILE, 'rb') as f:
		f.seek(0, os.SEEK_END)
		pointer = f.tell()
		buffer = b""

		while pointer > 0:
		#di chuyen con tro ngc doan chunk
			step = min(pointer, CHUNK_SIZE)
			pointer -= step
			f.seek(pointer)
		#doc chunk va ket hop buffer du thua
			chunk = f.read(step) + buffer
			lines = chunk.split(b'\n')
		#giu lai phan dong ko tron ven o dau chunk
			buffer = lines[0]
		#duyet cac dong tu duoi len
			for i in range(len(lines) -1, 0, -1):
				line = lines[i].decode('utf-8').strip()
				if not line:
					continue
			parts = line.split()
			if len(parts) < 5:
				continue
			#parse thoi gian
			try:
				log_time_str = parts[0].split('+')[0]
				log_time = datetime.fromisoformat(log_time_str)

				if log_time < target_time:
					#dung doc file khi vuot qua 1 phut
					print_results(protocols, ciphers, total_count)
					return
				#thong ke protocol va cipher
				protocols[parts[3]] += 1
				ciphers[parts[4]] += 1
				total_count += 1
			except ValueError:
				continue
	print_results(protocols, ciphers, total_count)
def print_results(protocols, ciphers, total_count):
	if total_count == 0:
		print("Ko co du lieu trong 1 phut")
		return
	print(f"--- THong ke SSL trong 1 phut qua (Tong: {total_count} requests) ---")

	print("\n[SSL Protocols]")
	for proto, count in protocols.items():
		percentage = (count / total_count) * 100
		print(f"{proto}: {percentage:.2f}% ({count})")

	print("\n{SSL Ciphers]")
	for cipher, count in ciphers.items():
		percent = (count / total_count) * 100
		print(f"{cipher}: {percentage:.2f}% ({count})")

if __name__ == "__main__":
	analyze_last_minute()
