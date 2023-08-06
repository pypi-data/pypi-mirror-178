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
import decimal
import os
from abc import ABC, abstractmethod


class EtherScan(ABC):

    BASE_URL = "https://api.etherscan.io/api"

    @abstractmethod
    def public_request(self, module: str, **kwargs):
        """
        Returns the response to the Etherscan API endpoint with the specified module, action, and apikey
        """

        # iterate through  combined dict of required arguments and kwargs passed
        # if a key appears in both operands (locals, kwargs), the last-seen value is kept
        if kwargs != dict():
            query_params = '?'
            param_dict = {'module': module} | kwargs

            for k, v in param_dict.items():
                query_params += f'{k}={v}&'
            query_params = query_params[:-1]

        else:
            query_params = ""

        resp = requests.get(EtherScan.BASE_URL + query_params)
        return resp.json()


class Stats(EtherScan):
    MODULE = 'stats'

    def __init__(self, etherscan_api_key: str):
        """
        etherscan_api_key (str): EtherScan API key. See https://docs.etherscan.io/getting-started/viewing-api-usage-statistics
        """
        self.etherscan_api_key = etherscan_api_key

    @classmethod
    def from_env(cls, abs_path: str, env_key: str = 'etherscan_api_key'):
        """
        Constructor overload to pass an API key via a .env file
        """
        dotenv_path = Path(abs_path)
        load_dotenv(dotenv_path=dotenv_path)
        etherscan_api_key = os.getenv(env_key)
        return cls(etherscan_api_key)

    @classmethod
    def from_key(cls, etherscan_api_key: str):
        """
        Constructor overload to pass an API key via a string.
        """
        return cls(etherscan_api_key)

    def public_request(self, module: str, **kwargs):
        return super().public_request(module, **kwargs)

    def get_ether_last_price(self, currency='usd'):
        """
        Returns the latest price of 1 ETH.

        Args:
            currency (float): Currency to return price of ETH in (either USD or BTC). Default is USD.
        """
        return float(super().public_request(Stats.MODULE,
                                            action='ethprice',
                                            apikey=self.etherscan_api_key)['result']['eth'+currency.casefold()])


class GasTracker(EtherScan):

    MODULE = 'gastracker'

    def __init__(self, web3: Web3, etherscan_api_key: str):
        """
        Args:
          web3 (Web3): Instance that will allow you to interact with the Ethereum blockchain. The easiest way is to use a remote node provider, such as Infura or Alchemy.
          etherscan_api_key (str): EtherScan API key. See https://docs.etherscan.io/getting-started/viewing-api-usage-statistics
        """
        self.w3 = web3
        self.etherscan_api_key = etherscan_api_key

    def public_request(self, module: str, **kwargs):
        return super().public_request(module, **kwargs)

    @classmethod
    def from_env(cls, web3: Web3, abs_path: str, env_key: str = 'etherscan_api_key'):
        """
        Constructor overload to pass an API key via a .env file
        """
        dotenv_path = Path(abs_path)
        load_dotenv(dotenv_path=dotenv_path)
        etherscan_api_key = os.getenv(env_key)
        return cls(web3, etherscan_api_key)

    @classmethod
    def from_key(cls, web3: Web3, etherscan_api_key: str):
        """
        Constructor overload to pass an API key via a string.
        """
        return cls(web3, etherscan_api_key)

    def get_estimation_of_confirmation_time(self, gasprice: str):
        """
        Returns the estimated time, in seconds, for a transaction to be confirmed on the blockchain.
        Note: The gas prices are returned in Gwei.

        #get-estimation-of-confirmation-time
        For details on the response format, see https://docs.etherscan.io/api-endpoints/gas-tracker

        Args:
            gasprice (str): Amount of gas being sent in Gwei (e.g. '2 Gwei')

        Returns:
            list[str]:
        """
        number, unit = gasprice.split(" ")
        gasprice_wei = self.w3.toWei(number, unit)
        print(gasprice_wei)

        return int(super().public_request(GasTracker.MODULE,
                                          action='gasestimate',
                                          gasprice=gasprice_wei,
                                          apikey=self.etherscan_api_key)['result'])

    def get_gas_oracle(self):
        """
        Returns the current Safe, Proposed, and Fast gas prices, the baseFee of the next pending block, and how busy the network is.

        For more details on the response format, see https://docs.etherscan.io/api-endpoints/gas-tracker#get-gas-oracle
        """
        return super().public_request(GasTracker.MODULE,
                                      action='gasoracle',
                                      apikey=self.etherscan_api_key)

    def get_safe_gas_price(self):
        """
        Returns the safe gas price from the gas oracle
        """
        return int(self.get_gas_oracle()['result']['SafeGasPrice'])

    def get_propose_gas_price(self):
        """
        Returns the propose gas price (average) from the gas oracle
        """
        return int(self.get_gas_oracle()['result']['ProposeGasPrice'])

    def get_fast_gas_price(self):
        """
        Returns the fast gas price (high priority) from the gas oracle
        """
        return int(self.get_gas_oracle()['result']['FastGasPrice'])

    def get_suggest_base_fee(self):
        """
        Returns the baseFee of the next pending block
        """
        return int(self.get_gas_oracle()['result']['suggestBaseFee'])

    def get_gas_used_ratio(self):
        """
        Retrns an estimate of how busy the network is
        """
        return float(self.get_gas_oracle()['result']['gasUsedRatio'])

    def get_max_total_gas_fee(self, gas_limit, max_fee_per_gas: str, currency='USD'):
        """
        Returns the maximum total gas fee the sender is willing to pay. Default is USD.
        """
        number, unit = max_fee_per_gas.split(" ")
        wei = gas_limit*self.w3.toWei(number, unit)
        print(wei)
        if currency.casefold() == 'wei':
            return number
        elif currency.casefold() == 'gwei':
            return self.w3.fromWei(wei, 'Gwei')
        elif currency.casefold() == 'ether':
            return self.w3.fromWei(wei, 'ether')
        elif currency.casefold() == 'usd':
            stats = Stats(self.etherscan_api_key)
            return float(self.w3.fromWei(wei, 'ether'))*stats.get_ether_last_price()

    def plot_gas_price_confirmation_time(self, gas: int, per_gas_price_increment: float = 0.5):
        """
        Plot the confirmation time against the total cost of gas in Gwei, Eth, and USD
        """
        safe = self.get_safe_gas_price()
        fast = self.get_fast_gas_price()
        propose = self.get_propose_gas_price()

        time_estimates = []

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
        fig.tight_layout(pad=2.0)
        fig.supylabel('confirmation time (s)')

        fee_per_gas_prices = np.array(
            np.arange(safe, fast, per_gas_price_increment))
        fee_per_gas_prices = np.append(fee_per_gas_prices, np.array(propose))
        for fee_per_gas in fee_per_gas_prices:
            time = self.get_estimation_of_confirmation_time(
                str(fee_per_gas) + ' Gwei')
            time_estimates.append(time)

        total_gas_prices = gas*fee_per_gas_prices
        total_gas_prices_eth = list(pd.Series(total_gas_prices).apply(
            lambda gas_price: self.w3.fromWei(self.w3.toWei(gas_price, 'Gwei'), 'Ether')).values)

        ax1.scatter(fee_per_gas_prices, time_estimates, color='b')
        ax1.set_xlabel('fee per unit gas price (Gwei)')
        ax1.set_ylabel('confirmation time (s)')

        ax2.scatter(total_gas_prices_eth, time_estimates, color='b')
        ax2.set_xlabel('total gas price (ETH)')
        ax2.set_ylabel('confirmation time (s)')

        stats = Stats(self.etherscan_api_key)
        total_gas_prices_usd = np.array(
            total_gas_prices_eth)*decimal.Decimal(stats.get_ether_last_price())

        ax3.scatter(total_gas_prices_usd, time_estimates, color='b')
        ax3.set_xlabel('total gas price (USD)')
        ax3.set_ylabel('confirmation time (s)')
