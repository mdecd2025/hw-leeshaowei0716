from waitress import serve
from flaskapp import app

# 使用 IPv6 地址和端口 8443 啟動 HTTPS 服務
serve(app, listen='[2001:288:6004:17:fff1:cd25:0000:b033]:8443', threads=8)
