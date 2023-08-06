import pandas as pd
import numpy as np
import time
from dotenv import load_dotenv
from web3 import HTTPProvider, Web3
import json
import websockets
import web3
from matplotlib import pyplot as plt
from pathlib import Path
import requests
import os
from abc import ABC, abstractmethod


class Tx(object):

    def __init__(self,
                 web3: Web3,
                 from_address: str,
                 to_address: str,
                 value: str,
                 max_fee_per_gas: str,
                 max_priority_fee_per_gas: str,
                 gas: int = 100_000,
                 chain_id: int = 1):
        """
        Args:
            web3 (Web3): Instance that will allow you to interact with the Ethereum blockchain. The easiest way is to use a remote node provider, such as Infura or Alchemy.
            to_address (str): The address to sender ether to.
            from_address (str): The sender address.
            value (str): The amount (in ether) to send to the address specified (e.g. '0.05 ether').
            gas (int): The maximum amount of gas you are willing to consume on a transaction.
            max_fee_per_gas (str): The maximum limit (in gwei) users are willing to pay for their transaction to be executed as str (e.g. 2 gwei). For a transaction to be executed, the max fee must exceed the sum of the base fee and the priority fee. The transaction sender is refunded max fee - (base fee + priority fee). Allows for transaction to execute and have user not worry about overpaying too far "beyond" the base fee when the transaction is executed.
            max_priority_fee_per_gas: Tip (in gwei) to incentivize miners to include a transaction in the block as str (e.g. 1 gwei). Without tips, miners would find it economically viable to mine empty blocks, as they would receive the same block reward. Under normal conditions, a small tip provides miners a minimal incentive to include a transaction. For transactions that need to get preferentially executed ahead of other transactions in the same block, a higher tip will be necessary to attempt to outbid competing transactions.
            chain_id: ID identifying the EVM network to connect to as int. See https://chainlist.org/ for a list.

        For more details on transaction parameters, see https://ethereum.org/en/developers/docs/gas/
        """
        self.w3 = web3
        # Check that there is no data corruption in the address string using toChecksumAddress() as an extra security measure
        # From address is public address of sender's account
        self.from_address = Web3.toChecksumAddress(from_address)
        # To address is public address of receiver account
        self.to_address = Web3.toChecksumAddress(to_address)

        number, unit = value.split(" ")
        self.value = self.w3.toWei(number, unit)
        self.gas = gas

        # To be eligible for inclusion in a block the offered price per gas must at least equal the base fee.
        # Base fee is value set by the protocol.
        # Use of EtherScan API's Gas Oracle "suggestBaseFee" is highly recommended. For more details, see https://docs.etherscan.io/api-endpoints/gas-tracker.
        number, unit = max_fee_per_gas.split(" ")
        self.max_fee_per_gas = self.w3.toWei(number, unit)

        number, unit = max_priority_fee_per_gas.split(" ")
        self.max_priority_fee_per_gas = self.w3.toWei(number, unit)

        self.nonce = self.w3.eth.get_transaction_count(self.from_address)
        self.chain_id = chain_id
        self.type = type

    def set_from_address(self, from_address: str):
        # Have to update the nonce when changing the from address because the nonce is dependent on the transction count of
        # the public address of the senders account
        self.from_address = Web3.toChecksumAddress(from_address)
        self.nonce = self.w3.eth.get_transaction_count(self.from_address)

    def get_from_address(self):
        return self.from_address

    def set_to_address(self, to_address: str):
        self.to_address = Web3.toChecksumAddress(to_address)

    def get_to_address(self):
        return Web3.toChecksumAddress(self.to_address)

    def set_value(self, value: str):
        number, unit = value.split(" ")
        self.value = self.w3.toWei(number, unit)

    def get_value(self):
        return self.get_value

    def get_gas(self):
        return self.gas

    def set_gas(self, gas: int):
        self.gas = gas

    def set_max_fee_per_gas(self, max_fee_per_gas: str):
        number, unit = max_fee_per_gas.split(" ")
        self.max_fee_per_gas = self.w3.toWei(number, unit)

    def set_max_priority_fee_per_gas(self, max_priority_fee_per_gas: str):
        number, unit = max_priority_fee_per_gas.split(" ")
        self.max_priority_fee_per_gas = self.w3.toWei(number, unit)

    def get_nonce(self):
        return self.nonce

    def as_dict(self):
        return {
            'to': self.to_address,
            'from': self.from_address,
            'value': self.value,
            'gas': self.gas,
            'maxFeePerGas': self.max_fee_per_gas,
            'maxPriorityFeePerGas': self.max_priority_fee_per_gas,
            'nonce': self.nonce,
            'chainId': self.chain_id
        }

    def sign_transaction(self, private_key: str):
        """
        Returns a transaction that’s been signed by the node’s private key, but not yet submitted.
        Submit the signed transaction using Tx.send_transaction.
        """
        transaction = self.as_dict()
        # Delete from key, prviate_key information is all that is needed
        del transaction['from']
        return self.w3.eth.account.sign_transaction(transaction, private_key)

    def send_raw_transaction(self, signed_tx):
        """
        Sends a signed and serialized transaction.

        Returns the transaction hash as a HexBytes object. 
        """
        return self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    def send_transaction(self):
        """
        Signs and sends the given transaction.

        Returns the transaction hash as a HexBytes object. 
        """
        transaction = self.as_dict()
        return self.w3.eth.send_transaction(transaction)
