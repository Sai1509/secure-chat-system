import socket
from Crypto.Cipher import AES

# Pre-shared key for simplicity
KEY = b"thisisasecretkey"  # 16 byte
 
def encrypt_message(message, key):
    # Create AES cipher for encryption
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return cipher.nonce + tag + ciphertext  # Combine nonce, tag, and ciphertext

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 65432))  # Connect to server
    print("Connected to server. Type 'exit' to quit.")

    while True:
        message = input("You: ")
        if message.lower() == 'exit':
            break
        encrypted_message = encrypt_message(message, KEY)
        client.sendall(encrypted_message)  # Send encrypted message

    client.close()
    print("Connection closed.")

if __name__ == "__main__":
    start_client()
