# Web3InternshipTask – Ethereum Crawler Web Application

## Description

This web application allows users to explore Ethereum wallet activity. Given a wallet address and a starting block, it displays:

- All **normal** and **internal transactions** from the given block to the latest.
- All **ERC-20 token transfers** involving the address.
- Historical **ETH and token balances** on a specified date (`YYYY-MM-DD` format).

## Technologies Used

- **APIs:**
  - [etherscan.io](https://etherscan.io)
  - [infura.io](https://infura.io)
- **Backend:**
  - Python
  - `web3.py`, `requests`, `Flask`, `Jinja2`
- **Frontend:**
  - Pure HTML & CSS

### Python Libraries

- `flask`
- `jinja2`
- `python-dotenv`
- `requests`
- `web3`

## Setup Instructions

1. **Clone the repository** and set up a Python virtual environment:

   ```bash
   git clone https://github.com/Grit-in/Web3InternshipTask
   cd Web3InternshipTask
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Setup the **.env** file and inside put
   ```bash
   ETHERSCAN_API_KEY=your_etherscan_api_key
   INFURA_URL=https://mainnet.infura.io/v3/your_infura_project_id
  
3. Install the requirements by running this command in the env

   ``` bash
   pip install -r req.txt 
   
4. Run the application with

   ```bash
   py app.py


### Warning for large amounts of data it will take a longer time to fetch everything so I added a print to show the progress it will show in the terminal/ide.
