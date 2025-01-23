import socket
from Crypto.Cipher import AES

# Pre-shared key for simplicity
KEY = b"thisisasecretkey"  # 16 bytes


def decrypt_message(encrypted_message, key):
    try:
        # Extract nonce, tag, and ciphertext from the message
        nonce = encrypted_message[:16]
        tag = encrypted_message[16:32]
        ciphertext = encrypted_message[32:]
        
        # Create AES cipher for decryption
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode('utf-8')
    except (ValueError, KeyError):
        return "[Decryption Failed]"

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
    server.bind(('localhost', 65432))  # Bind to localhost and port
    server.listen(1)
    print("Server is listening on port 65432...")

    conn, addr = server.accept()
    print(f"Connected by {addr}")

    while True:
        data = conn.recv(1024)  # Receive encrypted message
        if not data:
            break
        decrypted_message = decrypt_message(data, KEY)
        print(f"Client: {decrypted_message}")

    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    start_server()
