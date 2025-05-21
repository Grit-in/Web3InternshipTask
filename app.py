import os
from flask import Flask, render_template, request
import requests
from web3 import Web3
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()
app = Flask(__name__)

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
INFURA_URL = os.getenv("INFURA_URL")
web3 = Web3(Web3.HTTPProvider(INFURA_URL))


@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.fromtimestamp(int(value), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


def get_latest_block():
    return web3.eth.block_number


def get_block_by_timestamp(timestamp):
    low = 0
    high = get_latest_block()
    while low <= high:
        mid = (low + high) // 2
        block = web3.eth.get_block(mid)
        if block.timestamp < timestamp:
            low = mid + 1
        else:
            high = mid - 1
    return high


def get_eth_balance_at_block(address, block):
    balance_wei = web3.eth.get_balance(address, block_identifier=block)
    return web3.from_wei(balance_wei, 'ether')


def get_token_balance_at_block(address, token_address, block):
    erc20_abi = '[{"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}]'

    try:
        token_contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=erc20_abi)
        symbol = token_contract.functions.symbol().call()
        balance = token_contract.functions.balanceOf(address).call(block_identifier=block)
        try:
            decimals = token_contract.functions.decimals().call()
        except:
            decimals = 18
        balance_formatted = balance / (10 ** decimals)
        return {"symbol": symbol, "balance": round(balance_formatted, 7)}
    except:
        return None


def fetch_all_paged_data(url_base, address, start_block, end_block, label):
    all_results = []
    chunk_size = 10000
    current = start_block

    while current <= end_block:
        chunk_end = min(current + chunk_size - 1, end_block)
        url = f"{url_base}&address={address}&startblock={current}&endblock={chunk_end}&sort=asc&apikey={ETHERSCAN_API_KEY}"
        print(f"Fetching {label} txs: blocks {current} to {chunk_end}")
        response = requests.get(url)
        data = response.json()

        if data['status'] == '1':
            all_results.extend(data['result'])
        elif data['message'] == 'No transactions found':
            print(f"No {label} transactions in block range {current}-{chunk_end}")
        else:
            print(f"Error fetching {label} from {current} to {chunk_end}: {data['message']}")
            break

        current = chunk_end + 1

    print(f"Total {label} transactions fetched: {len(all_results)}")
    return all_results


@app.route('/', methods=['GET', 'POST'])
def index():
    transactions = []
    token_transfers = []
    historical_eth_balance = None
    historical_token_balances = []
    historical_date = None

    if request.method == 'POST':
        try:
            raw_address = request.form['address']
            address = Web3.to_checksum_address(raw_address)
        except Exception as e:
            return f"Invalid Ethereum address: {e}", 400

        start_block = int(request.form['start_block'])
        end_block = get_latest_block()
        historical_date = request.form.get('date')

        normal_txs = fetch_all_paged_data(
            "https://api.etherscan.io/api?module=account&action=txlist",
            address, start_block, end_block, "normal"
        )

        internal_txs = fetch_all_paged_data(
            "https://api.etherscan.io/api?module=account&action=txlistinternal",
            address, start_block, end_block, "internal"
        )

        token_transfers = fetch_all_paged_data(
            "https://api.etherscan.io/api?module=account&action=tokentx",
            address, start_block, end_block, "token"
        )

        for tx in normal_txs:
            tx['tx_type'] = 'normal'
            tx['value_eth'] = float(Web3.from_wei(int(tx['value']), 'ether'))

        for tx in internal_txs:
            tx['tx_type'] = 'internal'
            tx['value_eth'] = float(Web3.from_wei(int(tx['value']), 'ether'))

        for tx in token_transfers:
            try:
                tx['value_formatted'] = int(tx['value']) / (10 ** int(tx['tokenDecimal']))
            except:
                tx['value_formatted'] = 0

        transactions = sorted(normal_txs + internal_txs, key=lambda x: int(x['timeStamp']))

        if historical_date:
            dt = datetime.strptime(historical_date, "%Y-%m-%d")
            timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
            block_at_time = get_block_by_timestamp(timestamp)
            historical_eth_balance = get_eth_balance_at_block(address, block_at_time)

            token_addresses = list(set([tx['contractAddress'] for tx in token_transfers]))

            for token_addr in token_addresses:
                try:
                    checksummed_token_addr = Web3.to_checksum_address(token_addr)
                    token_info = get_token_balance_at_block(address, checksummed_token_addr, block_at_time)
                    if token_info:
                        historical_token_balances.append(token_info)
                except:
                    continue

        return render_template(
            'index.html',
            transactions=transactions,
            token_transfers=token_transfers,
            historical_eth_balance=historical_eth_balance,
            historical_token_balances=historical_token_balances,
            historical_date=historical_date
        )

    return render_template('index.html', transactions=[], token_transfers=[])


if __name__ == '__main__':
    app.run(debug=True)
