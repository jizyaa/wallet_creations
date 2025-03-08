from bip_utils import Bip39SeedGenerator, Bip44Coins, Bip44, base58, Bip44Changes
import logging

logging.basicConfig(
    filename='solana_account.txt',
    level=logging.INFO,
    format='%(message)s',
    filemode='w'
)

class BlockChainAccount():

    def __init__(self, mnemonic, coin_type=Bip44Coins.SOLANA) -> None:
        self.mnemonic = mnemonic.strip()
        self.coin_type = coin_type

    def get_address_pk(self):
        seed_bytes = Bip39SeedGenerator(self.mnemonic).Generate()
        
        if self.coin_type != Bip44Coins.SOLANA:
            bip44_mst_ctx = Bip44.FromSeed(seed_bytes, self.coin_type).DeriveDefaultPath()
            return bip44_mst_ctx.PublicKey().ToAddress(), bip44_mst_ctx.PrivateKey().Raw().ToHex()
        else:
            bip44_mst_ctx = Bip44.FromSeed(seed_bytes, self.coin_type)
            bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
            bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
            priv_key_bytes = bip44_chg_ctx.PrivateKey().Raw().ToBytes()
            public_key_bytes = bip44_chg_ctx.PublicKey().RawCompressed().ToBytes()[1:]
            key_pair = priv_key_bytes + public_key_bytes

            return bip44_chg_ctx.PublicKey().ToAddress(), base58.Base58Encoder.Encode(key_pair)

def read_mnemonics_from_file(file_path="mnemonic.txt"):
    """Read multiple mnemonics from a file, one per line."""
    try:
        with open(file_path, 'r') as file:
            mnemonics = [line.strip() for line in file if line.strip()]
        return mnemonics
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

# Example usage
if __name__ == "__main__":
    mnemonics = read_mnemonics_from_file("mnemonic.txt")
    
    if not mnemonics:
        print("No mnemonics found to process. Please create a mnemonic.txt file.")
    else:
        print(f"Processing {len(mnemonics)} mnemonics...")
        for idx, mnemonic in enumerate(mnemonics, 1):
            sol_account = BlockChainAccount(mnemonic, coin_type=Bip44Coins.SOLANA)
            try:
                sol_address, sol_private_key = sol_account.get_address_pk()
                logging.info(f"Address: {sol_address}")
                logging.info(f"Private Key: {sol_private_key}")
                print(f"Mnemonic {idx} processed successfully.")
            except Exception as e:
                logging.error(f"Error processing mnemonic {idx}: {e}")
                print(f"Error processing mnemonic {idx}: {e}")
