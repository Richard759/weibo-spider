import re

url = "//weibo.com/1766538387/KDuUGD450?refer_flag=1001030103_"
print(re.findall(r'//weibo.com/(\d+)/(.*)\?refer_flag=.*', url)[0][0])
