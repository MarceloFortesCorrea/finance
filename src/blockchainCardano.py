# BlockchainCardano.py

from pycardano import Address, Network
import requests as rqt


class BlockchainCardano:

    def __init__():
        global address

    def get_balance(address):
        addr = Address.decode("addr_test1vrm9x2zsux7va6w892g38tvchnzahvcd9tykqf3ygnmwtaqyfg52x")

        ada = Cardano("https://mainnet-node.cardano-mainnet.iohk.io:8443")
        address = address  # Endereço da conta Cardano
        balance = ada.balance(address)
        print("Balance:", balance, "lovelaces")
        return balance







