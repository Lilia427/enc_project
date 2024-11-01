# main.py
from flask import Flask, request, jsonify, render_template
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode

app = Flask(__name__)

def encrypt_ecb(plaintext, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = plaintext.ljust(16, ' ').encode()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return b64encode(encrypted).decode('utf-8')

def decrypt_ecb(ciphertext, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decoded_data = b64decode(ciphertext)
    decrypted = decryptor.update(decoded_data) + decryptor.finalize()
    return decrypted.decode('utf-8').strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    plaintext = data['plaintext']
    key = data['key'].ljust(16).encode()
    encrypted_text = encrypt_ecb(plaintext, key)
    return jsonify({'encrypted': encrypted_text})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    ciphertext = data['ciphertext']
    key = data['key'].ljust(16).encode()
    decrypted_text = decrypt_ecb(ciphertext, key)
    return jsonify({'decrypted': decrypted_text})

if __name__ == '__main__':
    app.run(debug=True)
