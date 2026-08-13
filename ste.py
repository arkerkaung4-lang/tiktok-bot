import threading
import requests

# Target URL (ကိုယ့်ရဲ့ Test Server ဖြစ်ရပါမယ်)
target_url = "http://localhost:8080"

def stress_test():
    while True:
        try:
            response = requests.get(target_url)
            print(f"Request sent! Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Connection failed: {e}")

# Threads တွေကို အသုံးပြုပြီး Request ပမာဏကို တိုးမြှင့်ခြင်း
thread_count = 50
for i in range(thread_count):
    thread = threading.Thread(target=stress_test)
    thread.start()

