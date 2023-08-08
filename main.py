from web3 import Web3
import cryptocompare
from wallets import wallets
from providers import providers

def get_balance(chain_name, provider_url, wallet_address):
    w3 = Web3(Web3.HTTPProvider(provider_url))

    if not w3.is_connected():
        print(f"Unable to connect to {chain_name} at {provider_url}")
        return None

    try:
        checksum_address = w3.to_checksum_address(wallet_address)
        balance_wei = w3.eth.get_balance(checksum_address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return balance_eth
    except Exception as e:
        print(f"Error fetching balance for address {wallet_address} on {chain_name}: {e}")
        return None

eth_price = cryptocompare.get_price('ETH', 'USD')['ETH']['USD']

wallet_balances = {}
total_in_usd = 0.0

for wid, (wallet_name, wallet_address) in wallets.items():
    wallet_balances[wallet_name] = {}

    for chain, provider_url in providers.items():
        balance = get_balance(chain, provider_url, wallet_address)
        if balance is not None:
            wallet_balances[wallet_name][chain] = balance
            total_in_usd += float(balance) * eth_price

for wallet_name, balances in wallet_balances.items():
    print(f"{wallet_name}:")
    for chain, balance in balances.items():
        balance_usd = float(balance) * eth_price
        print(f"{chain.capitalize()}: {balance} ETH (~${balance_usd:.2f})")
    print()

print(f"Total equivalent in USDT: ${total_in_usd:.2f}")
