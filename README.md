# Web3InternshipTask

## Etherium Crawler Web Application made in python

  ### Description
  
   &nbsp; This Web Application will take a wallet address along with a block and will show all normal and internal transactions from that to the latest
   &nbsp;&nbsp;block. Along with that the application will display all token transfers. The Web App will also take a date in the YYYY-MM-DD format and give &nbsp;&nbsp;you the balance of the adress in ETH and below will show all other tokens.

  ### Technologies used

  &nbsp; It uses etherscan.io and infura.io APIs for data. The Backend is made in python using web3.py and requests.py the Frontend is just pure html &nbsp;&nbsp;and css its connected to the Backend using Flash and jinja2.
  
&nbsp;&nbsp;Libs used:  
  &nbsp;  &nbsp;&nbsp;flask  
   &nbsp;  &nbsp;&nbsp;jinja2  
    &nbsp;  &nbsp;&nbsp;python-dotenv  
   &nbsp;  &nbsp;&nbsp;requests  
    &nbsp;  &nbsp;&nbsp;web3  

  ### Set-up
  &nbsp;  1. Download the folder from git or git clone it into a folder and setup a python virtual enviorment.
  
  &nbsp;  2. Set up an .env file in the Web3InternshipTask folder and insert your etherscan_api and infura_url in this format be sure its not set as .env.txt 
  &nbsp;&nbsp;but as a .env type file.
  
  ` ETHERSCAN_API_KEY=YOUR_ETHERSCAN_API_KEY`
  
   ` INFURA_URL=https://mainnet.infura.io/v3/your_infura_link`
   
  &nbsp; 3. In the same folder run the command in your enviorment ` pip install -r req.txt `

  &nbsp; 4. Run the command ` py app.py ` a dev server will open on a localhost address .
    
