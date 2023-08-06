# eth_transfer

Easily send transactions on the Ethereum blockchain and fine tune gas parameters.

# Motivation

The [Web3.py](https://web3py.readthedocs.io/en/v5/) python library, Alchemy API, and a slew of other projects provide easy ways to send transactions (exchange of value between addresses). However, there is often a lot of guess work that goes into selecting the values affecting the total gas fee, such as the max priority fee per gas, the max fee per gas, and the maximum amount of gas the user is willing to be consumed for the transaction to succeed. The Etherum network can become very busy at certain times (i.e. days following the FTX bankruptcy) and thus gas fees become very large. User controls on gas on applications such as MetaMask are basic, and give vaugue time estimates when trying to save on gas fees.

This package intends to provide an easy to use and customizable object oriented way to send transactions that minimize gas fees according to your needs.

# How to use

The use of this package requires you are able to connect to the Etherum blockchain using web3.py and also have an Etherscan account from which you can create an API key. Access to PRO Etherscan endpoints is <b>not</b> neeeded.

## Installing web3

If you do not have the web3 package installed in your environment or virtual environment, follow the quickstart [here](https://web3py.readthedocs.io/en/v5/quickstart.html). 

If you do not have an Etherscan account, create one as well as an API key by following the Getting Started steps [here](https://docs.etherscan.io/getting-started/creating-an-account).

# Quickstart

You can install the <code>eth_transfer</code> package via pip

```
pip3 install eth_transfer
```

## Sending a Transaction

After you have installed the package, create a <code>Web3</code> instance using either a local or remote provider. Below, we use the Remote provider Infura.io as an example.

```python 
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/YOUR_PROJECT_ID"))
```

Instantiate an instance of the <code>Tx</code> class

```python
address_1 = SENDING_ADDRESS
address_2 = RECEIVING_ADDRESS

transaction = Tx(w3, address_1, address_2, '0.100 ether', '55 gwei', '1 gwei')
```

Now, send the transaction

```python
transaction.send_transaction()
```

## Tracking Gas Prices

Instantiate an instance of the <code>GasTracker</code> class. This can be done 
one of two ways. Both ways are shown below

<li>From variable with string of your API key

```python
etherscan_key = YOUR_ETHERSCAN_KEY
gastracker = GasTracker.from_key(etherscan_key)
```

</li>

<li> From env with your API Key

```python
fpath = FILEPATH_TO_ENV_WITH_API_KEY # e.g. '/Users/DeadBeef/Desktop/etherscan.env'
key_name = ENV_API_KEY_NAME # e.g. 'API_KEY'
gastracker = GasTracker.from_env(fpath, key_name)
```

</li>

### Confirmation Times vs. Fee Per Gas

```python
gas_limit = 50000 # Note: minimum is 21,000 
gastracker.plot_gas_price_confirmation_time(gas_limit)
```

### Sending a slow transaction 

Sometimes, you can wait for a transaction to be confirmed! If so, you might as well save ETH on it being confirmed. Note, the maximum fee per gas you are willing to pay must exceed the current base fee. This is taken care of for you.

```python
gastracker.get_safe_gas_price()
```














