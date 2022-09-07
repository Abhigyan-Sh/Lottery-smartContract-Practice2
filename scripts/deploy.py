from brownie import Smart_lottery, network, config
from scripts.helpful_scripts import getAccount, get_contract
from web3 import Web3
import time

def deployer():
    Smart_lottery.deploy(
        get_contract("vrfCoordinator").address,
        get_contract("link").address,
        config(["network"][network.show_active()]["KeyHash"]),
        config(["network"][network.show_active()]["fee"]),
        get_contract("ethTo_usd_priceFeed").address,
        {"from": getAccount()}
        )

def starter():
    lottery= Smart_lottery[-1]
    txn= lottery.start_lottery({"from": getAccount()})
    txn.wait(1)
    print('super, la loterie a commencé!')

def enter():
    lottery= Smart_lottery[-1]
    txn= lottery.participate({"from": getAccount(), "value": lottery.entranceFee()+ 10000000})
    txn.wait(1)
    print('vous êtes inscrit à la loterie')

def ending():
    print("funding with 'link' tokens to our lottery contract!")
    # 
    # @dev::: went on to linkToken etherscan rinkeby network and in interaction section found function transfer() 
    # @dev::: then transfered to my smartcontract Smart_lottery no not from gui right there but came here and did through programming..
    # 
    LinkToken= get_contract("ethTo_usd_priceFeed")
    lottery= Smart_lottery[-1]
    LinkToken.transfer(lottery.address, Web3.toWei(0.1, "ether"), {"from": getAccount()})
    # 
    print("funding with 'link' tokens to our lottery contract!")
    # 
    # @dev::: linkToken is a contract which has a supply of 1 Billion LinkTokens and thus it can transfer() us those tokens
    # 
    txn= lottery.end_lottery({"from": getAccount()})
    txn.wait(1)
    time.sleep(60)
    print(f'{lottery.recentWinner} est le récent gagnant!!')
    # 
# @dev::: when our smartContract has to interact with other smartContracts then:
# @dev::: our contract just simply needs address of those other smart Contracts to interact with them like Reggie had address of verra and took with herself link
# @dev::: when we have to interact with other smart contract:
  # @dev::: we either:-
    # @dev::: import those contracts, make obj. of that smartContract like vrfCoordinator contract
    # @dev::: while sometimes we make those smart Contracts by taking their addresses and abi and name and then we interact.
    # @dev::: or we make interfaces of those contracts like IWeth.
    # 
def main():
    deployer()
    starter()
    enter()
    ending()