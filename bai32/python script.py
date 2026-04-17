import sys

for line in sys.stdin:
    line = line.strip()
    line_tach = line.split('"')
    if len(line_tach) > 5:
        first_part = line_tach[0].find('[')
        second_part = line_tach[0].find(']')
        date_time = line_tach[0][first_part+1 : second_part]
        
        date_only = date_time.split()[0]
        
        before = line_tach[0][:first_part].strip()
        before_tach = before.split()
        line_teo = line_tach[2].split()
        
        host = before_tach[0]
        ident = before_tach[1]
        authuser = before_tach[2]
        date = f"[{date_only}]" 
        request = f'"{line_tach[1]}"' 
        status = line_teo[0]
        bytes = line_teo[1]
        
        result = f"{host}\n {ident}\n {authuser}\n {date}\n {request}\n {status}\n {bytes}\n"
        print(result)