import os
import json
import requests
import threading
import time
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

CACHE_FILE = 'username_cache.json'
checked_usernames = set()
taken_usernames = []
available_usernames = []
lost_usernames = []
other_usernames = []
lock = threading.Lock()
stop_flag = threading.Event()
current_username = ""
thread_running = False
username_generator = None  # Keep generator persistent between starts

# Load cache
if os.path.exists(CACHE_FILE):
  with open(CACHE_FILE, 'r') as f:
    try:
      data = json.load(f)
      checked_usernames = set(data.get("checked", []))
      available_usernames = data.get("available", [])
    except json.JSONDecodeError:
      print("[!] Failed to load cache")

def save_cache():
  with lock:
    with open(CACHE_FILE, 'w') as f:
      json.dump({
        "taken": taken_usernames,
        "available": available_usernames,
        "lost": lost_usernames,
        "other": other_usernames
      }, f, indent=2)

def check_username(name):
  global current_username
  current_username = name

  if name in checked_usernames:
    return

  try:
    headers = {
    "User-Agent": "https://github.com/redbackspider69/MCNameAvailabilityChecker"
    }
    res = requests.get(f"https://playerdb.co/api/player/minecraft/{name}", headers=headers, timeout=5)
    print(f"Checking {name} → {res.status_code}")

    with lock:
      checked_usernames.add(name)

      if res.status_code == 200:
        print(f"[TAKEN] {name}")
        taken_usernames.append(name)
      elif res.status_code == 429:
        print(f"[RATE-LIMITED] {name}")
        lost_usernames.append(name)
      elif res.status_code == 404:
        print(f"[AVAILABLE] {name}")
        available_usernames.append(name)
      else:
        print(f"[UNKNOWN] {name}")
        other_usernames.append(name)

    save_cache()

  except Exception as e:
    print(f"[ERROR] {name}: {e}")
    with lock:
      checked_usernames.add(name)
    save_cache()

def generate_usernames():
  from itertools import product
  import string
  charset = string.ascii_lowercase + string.digits + "_"
  for r in (3, 4):
    for combo in product(charset, repeat=r):
      yield ''.join(combo)
      print(combo)

def start_checking():
  global thread_running, username_generator

  print("[*] Background thread started")
  thread_running = True

  if username_generator is None:
    username_generator = generate_usernames()

  for name in username_generator:
    if stop_flag.is_set():
      print("[!] Stop flag detected")
      break
    check_username(name)
    time.sleep(1)

  thread_running = False

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/start', methods=['POST'])
def start():
  global thread_running, stop_flag
  if not thread_running:
    stop_flag.clear()
    threading.Thread(target=start_checking, daemon=True).start()
    return jsonify({"status": "started"})
  return jsonify({"status": "already running"})

@app.route('/stop', methods=['POST'])
def stop():
  stop_flag.set()
  return jsonify({"status": "stopped"})

@app.route('/usernames')
def usernames():
  return jsonify({
    "available_usernames": available_usernames, 
    "lost_usernames": lost_usernames, 
    "other_usernames": other_usernames, 
    "taken_usernames": taken_usernames
    })

@app.route('/status')
def status():
  return jsonify({"current": current_username})

if __name__ == '__main__':
  app.run(debug=True)