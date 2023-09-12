from config import *
from sql_scripts import *
from datetime import datetime
from moralis import evm_api


chains = {
    '0x38' : 'bsc',
    '0x1' : 'eth',
    '0x89' : 'polygon',
}


dct = {
    'thx_alert_erc20_in' : "🚨🐳 WHALE ALERT - {}`s WALLET 🐳🚨\nTransaction Type: ERC-20\n\nWallet Address: {}\n\n⬇️ IN Transaction Hash: {}\n\nContract Address: {}\n\nTimestamp: {}\n\nTotal USD Value: ${}",
    'thx_alert_erc20_out' : "🚨🐳 WHALE ALERT - {}`s WALLET 🐳🚨\nTransaction Type: ERC-20\n\nWallet Address: {}\n\n⬆️ OUT Transaction Hash: {}\n\nContract Address: {}\n\nTimestamp: {}\n\nTotal USD Value: ${}",
    'stop_bot' : "🤖 You have stopped the bot. To launch, use the /launch_bot command 🤖",
    'launch_bot' : "🤖 You have successfully launched the bot. 🤖",
    'add_wallet_image' : "📸 You have successfully added a photo 📸\n\nTo crypto wallet with the following blockchain address:\n{}",
    'thx_alert_native_in' : '🚨🐳 WHALE ALERT - {}`s WALLET 🐳🚨\nTransaction Type: NATIVE\n\nWallet Address: {}\n\n⬇️ IN Transaction Hash: {} ({} ({}))\n\nTimestamp: {}\n\nTotal USD Value: ${}',
    'thx_alert_native_out': '🚨🐳 WHALE ALERT - {}`s WALLET 🐳🚨\nTransaction Type: NATIVE\n\nWallet Address: {}\n\n⬆️ OUT Transaction Hash: {} ({} ({}))\n\nTimestamp: {}\n\nTotal USD Value: ${}',
}


transfer_info ={
    'bsc' : ['BNB', 'https://bscscan.com/tx/', '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'],
    'eth' : ['ETH', 'https://etherscan.io/tx/', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'],
    'polygon' : ['MATIC', 'https://polygonscan.com/tx/', '0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0'],
}

