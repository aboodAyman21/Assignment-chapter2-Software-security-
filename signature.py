from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

def main():
    print("--- RSA Digital Signature Demonstration in Python ---")
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    print("[+] RSA Key Pair Generated Successfully.")

    message = b"This is an official document: Transfer $1000 to Alice."
    print(f"[+] Original Message: {message.decode()}")

    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print(f"[+] Generated Signature (Hex preview): {signature.hex()[:50]}...")
    print("[+] Message successfully signed using Private Key.")

    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("[+] SUCCESS: The signature is VALID!")
    except Exception as e:
        print(f"[-] FAILURE: The signature is INVALID! Details: {e}")

    tampered_message = b"This is an official document: Transfer $1000 to Oscar."
    print(f"\n[+] Tampered Message: {tampered_message.decode()}")
    
    try:
        public_key.verify(
            signature,
            tampered_message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("[+] SUCCESS: The signature is VALID!")
    except Exception as e:
        print(f"[-] FAILURE: Signature verification failed for tampered message as expected! ({e})")

if __name__ == "__main__":
    main()