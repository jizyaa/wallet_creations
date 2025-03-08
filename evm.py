import logging
from eth_account import Account
from mnemonic import Mnemonic

Account.enable_unaudited_hdwallet_features()

logging.basicConfig(
    filename="created_wallets.txt",
    level=logging.INFO,
    format="Address: %(address)s\nMnemonic: %(mnemonic)s\nPrivate Key: %(private_key)s\n",
    filemode='a'
)

def generate_wallet():
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=128)
    account = Account.from_mnemonic(mnemonic)
    address = account.address
    private_key = account.key.hex()
    return address, mnemonic, private_key

def log_wallet(address, mnemonic, private_key):
    """Log wallet details to the file."""
    logging.info("", extra={"address": address, "mnemonic": mnemonic, "private_key": private_key})

def main():
    try:
        wallet_count = int(input("How many wallets do you want to generate? "))
        if wallet_count <= 0:
            print("Invalid number of wallets. Please enter a positive integer.")
            return

        for _ in range(wallet_count):
            address, mnemonic, private_key = generate_wallet()
            log_wallet(address, mnemonic, private_key)

        print(f"{wallet_count} wallets generated and logged to 'created_wallets.txt'.")

    except ValueError:
        print("Please enter a valid numeric input.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
