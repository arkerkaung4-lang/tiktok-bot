#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys
from pathlib import Path

# ကျောင်းအုပ်စုပုံ ဖိုင်ရှိသည့် directory သို့ ပြောင်းရန်
os.chdir('/home/ubuntu/qr_image_viewer/public')

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

# Server စတင်ရန်
PORT = 8000
server_address = ('', PORT)
httpd = HTTPServer(server_address, MyHTTPRequestHandler)

print("=" * 60)
print("🚀 QR Code Image Viewer Server စတင်ပြီးပါပြီ!")
print("=" * 60)
print(f"📱 Local URL: http://localhost:{PORT}")
print(f"🌐 Public URL: https://qr-image-viewer.manus.im")
print(f"📂 ဖိုင်ရှိသည့် Directory: {os.getcwd()}")
print("=" * 60)
print("🛑 Server ရပ်ရန်: Ctrl+C ကိုနှိပ်ပါ")
print("=" * 60)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n🛑 Server ရပ်ပြီးပါပြီ။")
    sys.exit(0
