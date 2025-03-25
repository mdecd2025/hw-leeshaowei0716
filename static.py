from flask import Flask, send_from_directory
from flask_talisman import Talisman  # 引入 Flask-Talisman
import ssl
from threading import Thread

# 初始化 Flask 應用
app = Flask(__name__)

# 初始化 Flask-Talisman，設置安全配置
talisman = Talisman(app)

# 強制所有 HTTP 請求重定向到 HTTPS
talisman.force_https = True

# 設置安全 HTTP 頭部（例如：防止跨站腳本攻擊等）
talisman.content_security_policy = {
    'default-src': ["'self'"],
    'script-src': ["'self'", "trusted-cdn.com"],
    'style-src': ["'self'", "trusted-cdn.com"]
}

# Route to serve the index.html file
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Route to serve static files from the ./cmsimde/static directory
@app.route('/cmsimde/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('cmsimde/static', filename)

# Route to serve other HTML files from the root directory
@app.route('/<path:filename>')
def serve_html(filename):
    return send_from_directory('.', filename)

# 啟動 HTTP 服務（端口 8000）
def run_http():
    app.run(host='2001:288:6004:17:fff1:cd25:0000:b033', port=8000, debug=True, use_reloader=False)

# 啟動 HTTPS 服務（端口 8443）
def run_https():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='localhost.crt', keyfile='localhost.key')  # 加載證書和私鑰
    app.run(host='2001:288:6004:17:fff1:cd25:0:b053', port=8443, debug=True, ssl_context=context, use_reloader=False)

if __name__ == '__main__':
    # 分別在不同的線程上啟動 HTTP 和 HTTPS 服務
    http_thread = Thread(target=run_http)
    https_thread = Thread(target=run_https)

    http_thread.start()
    https_thread.start()
