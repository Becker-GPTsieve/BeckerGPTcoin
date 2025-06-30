
import hashlib
import time
import json
import rsa
import os

class BeckerGPTWallet:
    def __init__(self):
        (self.pubkey, self.privkey) = rsa.newkeys(512)

    def sign(self, message):
        return rsa.sign(message.encode(), self.privkey, "SHA-256")

    def get_public_key(self):
        return self.pubkey.save_pkcs1().decode()

class BeckerGPTTransaction:
    def __init__(self, sender, recipient, amount, signature):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'signature': self.signature.hex()
        }

    def hash(self):
        tx_str = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(tx_str.encode()).hexdigest()

class BeckerGPTBlock:
    def __init__(self, index, transactions, previous_hash, timestamp=None):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class BeckerGPTBlockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = BeckerGPTBlock(0, [], "0")
        self.chain.append(genesis_block)

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        block = BeckerGPTBlock(len(self.chain), self.pending_transactions, self.chain[-1].hash)
        self.chain.append(block)
        self.pending_transactions = []

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.hash != curr.compute_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True

# Interface
def main():
    print("🔐 Criando sua carteira BeckerGPT...")
    wallet = BeckerGPTWallet()
    print("✅ Carteira criada com sucesso!
")
    print("🔑 Chave Pública:")
    print(wallet.get_public_key())

    recipient = input("🧾 Endereço do destinatário (pode ser nome simbólico): ")
    amount = float(input("💰 Quantia BeckerGPT para enviar: "))

    message = f"{wallet.get_public_key()}->{recipient}:{amount}"
    signature = wallet.sign(message)

    transaction = BeckerGPTTransaction(
        sender=wallet.get_public_key(),
        recipient=recipient,
        amount=amount,
        signature=signature
    )

    print("\n📦 Transação criada e assinada!")
    print("📝 Hash da transação:", transaction.hash())

    blockchain = BeckerGPTBlockchain()
    blockchain.add_transaction(transaction)
    blockchain.mine_pending_transactions()

    print("\n🧱 Bloco minerado com sucesso. Blockchain atual:")
    for block in blockchain.chain:
        print(f"📦 Bloco {block.index} | Hash: {block.hash}")

    print("\n🔗 Blockchain válida?", blockchain.is_chain_valid())

if __name__ == "__main__":
    main()
