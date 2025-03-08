import random
from mnemonic import Mnemonic
from nacl.signing import SigningKey
from hashlib import blake2b

def generate_sui_wallet():
    # Create a mnemonic phrase (12 words)
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=128)
    print(f"Mnemonic: {words}")
    
    seed = mnemo.to_seed(words)
    print(f"Seed (hex): {seed.hex()}")
    
    private_key_bytes = seed[:32]
    signing_key = SigningKey(private_key_bytes)
    private_key_hex = private_key_bytes.hex()
    print(f"Private Key (hex): {private_key_hex}")
    
    public_key_bytes = bytes(signing_key.verify_key)
    print(f"Public Key (hex): {public_key_bytes.hex()}")
    
    signature_scheme_flag = b"\x00"
    data_to_hash = signature_scheme_flag + public_key_bytes
    print(f"Data to hash (flag + pubkey, hex): {data_to_hash.hex()}")
    
    blake2b_hash = blake2b(digest_size=32)
    blake2b_hash.update(data_to_hash)
    address_bytes = blake2b_hash.digest()
    print(f"BLAKE2b Hash (hex): {address_bytes.hex()}")
    
    address = "0x" + address_bytes.hex()
    print(f"Generated Address: {address}")
    
    return address, private_key_hex, words

def generate_wallets():
    try:
        num_wallets = int(input("How many wallets do you want to create? "))
        if num_wallets <= 0:
            print("Please enter a positive integer.")
            return
        
        with open("createdsui.txt", "w") as f:
            for _ in range(num_wallets):
                address, private_key, mnemonic = generate_sui_wallet()
                f.write(f"Address: {address}\nPrivate Key: {private_key}\nMnemonic: {mnemonic}\n\n")
        
        print(f"Successfully generated {num_wallets} wallets. Data saved to 'createdsui.txt'.")
    
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_wallets()
