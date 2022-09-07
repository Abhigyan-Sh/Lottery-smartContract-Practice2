from mimetypes import init
from brownie import (
    accounts, network, 
    config, Contract, 
    MockV3Aggregator, VRFCoordinatorMock, LinkToken
    )

LOCAL_DEVELOPMENT_NETWORK= ["mainnet-fork-dev", "mainnet-fork", "development"]

def getAccount(id= None, index= None):
    if id:
        return accounts.load(id)
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_DEVELOPMENT_NETWORK:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def get_contract(contract_name):
    contractToMock= {
        "ethTo_usd_priceFeed": MockV3Aggregator,
        "vrfCoordinator": VRFCoordinatorMock,
        "link": LinkToken
    }
    contract_type= contractToMock[contract_name]
    if network.show_active() in LOCAL_DEVELOPMENT_NETWORK:
        if len(contract_name)<= 0:
            deploy_mocks()
        contract= contract_name[-1]
    else:
        contract_address= config['networks'][network.show_active()][contract_name]
        contract= Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract

decimal= 8
initial_answer= 200000000000

def deploy_mocks():
    MockV3Aggregator.deploy(decimal, initial_answer,{"from":getAccount()})
    print('deployed MockV3Aggregator !')
    linkToken= LinkToken.deploy({"from":getAccount()})
    print('deployed LinkToken !')
    VRFCoordinatorMock.deploy(linkToken.address, {"from":getAccount()})
    print('deployed VRFCoordinatorMock !')
    print('deployed mocks!')
    # since these are deployments so didn't needed txn.wait(1) or wait for 1 block confirmation
# 