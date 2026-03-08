# caesar_final.py
# Robust, fixed Caesar cipher program — ready to run

def get_double_alphabet(alphabet: str) -> str:
    """Return alphabet concatenated with itself (for demonstration)."""
    return alphabet + alphabet

def get_message(prompt: str = "Please enter a message to encrypt: ") -> str:
    """Read a message from the user."""
    return input(prompt)

def get_cipher_key(prompt: str = "Please enter a key (whole number from 1-25): ") -> int:
    """
    Read and validate a cipher key from the user.
    Ensures an integer in range 1..25 is returned.
    """
    while True:
        user = input(prompt).strip()
        try:
            key = int(user)
        except ValueError:
            print("Invalid input — enter an integer between 1 and 25.")
            continue
        if 1 <= key <= 25:
            return key
        print("Key out of range — please enter a whole number from 1 to 25.")

def encrypt_message(message: str, cipher_key: int, alphabet: str) -> str:
    """
    Encrypt message using Caesar cipher.
    - Converts message to uppercase.
    - Leaves non-alphabet characters unchanged (spaces, punctuation, digits).
    - Uses modulo arithmetic so both positive and negative shifts work correctly.
    """
    uppercase = message.upper()
    encrypted = []
    alpha_len = len(alphabet)

    for ch in uppercase:
        if ch in alphabet:
            pos = alphabet.index(ch)                 # 0..25
            new_pos = (pos + cipher_key) % alpha_len
            encrypted.append(alphabet[new_pos])
        else:
            encrypted.append(ch)
    return "".join(encrypted)

def decrypt_message(message: str, cipher_key: int, alphabet: str) -> str:
    """Decrypt by encrypting with the negative of the key."""
    return encrypt_message(message, -cipher_key, alphabet)

def run_caesar_cipher_program():
    my_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    double_alpha = get_double_alphabet(my_alphabet)

    print("Alphabet:", my_alphabet)
    print("Double Alphabet (demo):", double_alpha)

    message = get_message("Please enter a message to encrypt/decrypt: ")
    print("Original message:", message)

    key = get_cipher_key()
    print("Cipher key:", key)

    encrypted = encrypt_message(message, key, my_alphabet)
    print("Encrypted Message:", encrypted)

    decrypted = decrypt_message(encrypted, key, my_alphabet)
    print("Decrypted Message:", decrypted)

if __name__ == "__main__":
    run_caesar_cipher_program()
