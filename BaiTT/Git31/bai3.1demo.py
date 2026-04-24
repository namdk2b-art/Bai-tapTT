
from user_agents import parse
# Dictionary lưu số lượt truy cập của từng trình duyệt
dict_browser = {}

file_path = r"I:/BaiTT/Git31/doc/gistfile1.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    
    for line in file:
        # Duyệt từng dòng log (mỗi dòng = 1 lượt truy cập)
        parts = line.split('"')
        # Tách dòng log theo dấu " → tạo list các thành phần
        if len(parts) > 5: 
             # Kiểm tra dòng có đủ thành phần để lấy user agent
            user_agent = parts[5]
            # Lấy chuỗi User-Agent
            #print(user_agent)
            browser = parse(user_agent).browser.family
            # Phân tích User-Agent để lấy thông tin trình duyệt
            dict_browser[browser] = dict_browser.get(browser, 0) + 1
            # Cập nhật số lượt truy cập cho trình duyệt trong dictionary
        
print(dict_browser)
total = sum(dict_browser.values())
#tính tổng số lượt truy cập
sorted_percent = sorted(dict_browser.items(), key=lambda x: x[1], reverse=True)
#sắp xếp trình duyệt theo số lượt truy cập giảm dần
print("Trinh duyet theo ty le giam dan:")
for browser, count in sorted_percent:
    percent = (count / total) * 100
    print(f"{browser}: {percent:.2f}%")







