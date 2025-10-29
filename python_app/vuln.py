# vuln_app.py
# Intentionally vulnerable example for static analysis testing only.

import sqlite3
import subprocess
import pickle
import hashlib
import random
import requests

# 1) Hard-coded secret (Secret in code)
API_TOKEN = "super-secret-token-12345"

# 2) Weak randomness used for token generation
def generate_token_weak():
    return str(random.random()).replace("0.", "")[:8]

# 3) Weak hashing (MD5) for "passwords"
def store_password_weak(username, password):
    h = hashlib.md5(password.encode()).hexdigest()
    with open("users.txt", "a") as f:
        f.write(f"{username}:{h}\n")

# 4) Insecure SQL construction — SQL injection vulnerability
def get_user_from_db(username):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    # unsafe: string concatenation with untrusted input
    query = "SELECT id, name FROM users WHERE username = '%s';" % username
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    return result

# 5) Command injection via shell=True and unsanitized input
def list_files(user_supplied_path):
    # DO NOT use shell=True with untrusted input
    cmd = "ls " + user_supplied_path
    subprocess.call(cmd, shell=True)

# 6) Dangerous eval of input
def compute(expression):
    # DO NOT eval untrusted expressions
    return eval(expression)

# 7) Insecure deserialization with pickle
def load_pickle(data_bytes):
    # Do not unpickle untrusted data
    return pickle.loads(data_bytes)

# 8) Insecure HTTP request (TLS verification disabled)
def fetch_url_insecure(url):
    # verify=False disables TLS certificate verification
    return requests.get(url, verify=False).text

if __name__ == "__main__":
    # Example flows for test only (not meant for real use)
    print("Generated weak token:", generate_token_weak())

    store_password_weak("alice", "password123")

    # Simulate SQL injection test
    print("DB lookup:", get_user_from_db("alice'; --"))

    # Simulate command injection test
    # (DON'T provide a dangerous path when testing)
    # list_files("; echo hacked")

    # Dangerous eval usage
    # print("Eval result:", compute("__import__('os').getcwd()"))

    # Dangerous pickle usage (commented out for safety)
    # print(load_pickle(b""))  # placeholder

    # Insecure fetch (for testing static analysis only)
    # print(fetch_url_insecure("https://example.com"))