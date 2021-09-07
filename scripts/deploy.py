from brownie import VestingEscrowSimple, VestingEscrowFactory, ERC20, accounts, chain, Contract
from datetime import datetime
YEAR = 365 * 86400

STARTTIME = 1630676799

VESTING_ESCROWS = [
    {
        "duration": 4 * YEAR,
        "start": STARTTIME,
        "cliff": YEAR,
        "recipients": {
            "0xBC5b552641e5d203f0a6C230aA9dC14DA7450053" : 221250000 * 10 ** 18,
            "0x7932810A66FEdc6c72a2578Fc83F44521832DEC2" : 101250000 * 10 ** 18,
            "0x187089B33E5812310Ed32A57F53B3fAD0383a19D" : 7500000 * 10 ** 18,
            "0xced608aa29bb92185d9b6340adcbfa263dae075b" : 37500000 * 10 ** 18,
            "0x775aF9b7c214Fe8792aB5f5da61a8708591d517E" : 7500000 * 10 ** 18,
            "0xd26a3F686D43f2A62BA9eaE2ff77e9f516d945B9" : 7500000 * 10 ** 18,
            "0xb4C3A698874B625DF289E97f718206701c1F4c0f" : 7500000 * 10 ** 18,
            "0x6094Fb01F02BB47db10DD7c61c4320fd185D27f3" : 7500000 * 10 ** 18,
            "0x7715963f334fc9e593fb938198A1976F08e95DAa" : 37500000 * 10 ** 18,
            "0x36f94ceD6Ec251c5608180BEfD01332Ef0A6A521" : 7500000 * 10 ** 18,
            "0x0573e05d9650836bB85CF26A4BD6C1b8eF7E99be" : 307500000 * 10 ** 18
        },
    },
]

def main():
    # Remember to create the account 'admin' with:
    # brownie accounts new admin
    # Enter the private key
    # Set a password to encrypt it (will be required to load)

    admin = accounts.load('admin')

    # ERC20 has to be created and in property of the admin account.
    total_amount = sum(sum(x["recipients"].values()) for x in VESTING_ESCROWS)
    # minting is already done, check out balance > total_amount || approval > total_amount
    token = ERC20.at("0x6e65178dbeed0b264dc8bf83334a02ade8a8f190") # fake token, use FRAK
    # token._mint_for_testing(total_amount)
    # Otherwise give approval externally and then run the script.
    print('Total amount to distribute: ',total_amount)

    #######################

    factory = Contract.from_explorer('')
    # CONTRACTS
    # https://github.com/banteg/yearn-vesting-escrow
    # rinkeby
    # VestingEscrowFactory: 0x2836925b66345e1c118ec87bbe44fce2e5a558f6
    # VestingEscrowSimple: 0x8bb4edaf9269a3427ede1d1ad1885f6f9d5731f5

    # mainnet
    # VestingEscrowFactory: 0xF124534bfa6Ac7b89483B401B4115Ec0d27cad6A
    # VestingEscrowSimple: 0x9c351CabC5d9e1393678d221F84E6EE3D05c016F
##############################
    # use created factory and template (then add those of mainnet)
    # template = VestingEscrowSimple.deploy({"from": admin})
    # factory = VestingEscrowFactory.deploy(template, {"from": admin})
##############################
    # factory deployed in tests: 0xFAa6b92Ca7c6C16FEa6Cb76F8052ae8EE97D8be6
#########################################################################

    # This is token approval for the factory contract
    token.approve(factory, total_amount, {'from': admin})

    for x in VESTING_ESCROWS:
        print("---------------------------------------------------------------")
        for recipient, amount in x["recipients"].items():
            print('For ',recipient,' are locked ',amount)
            tx = factory.deploy_vesting_contract(
                token,
                recipient,
                amount,
                x["duration"],
                x["start"],
                x["cliff"],
                {'from': admin}
            )
            print("---------------------------------------------------------------")

# BROWNIE ON RINKEBY
 # tx do not return parameters and the below code fails..
            # escrow = VestingEscrowSimple.at(tx.new_contracts[0])
            # assert token.balanceOf(escrow) == amount
            # assert escrow.recipient() == recipient
            # print('Vesting deployed to ',tx.new_contracts[0])
            # print('Beneficiary: ', recipient)
            # print("Locked: ", escrow.locked().to("ether"))
            # date_time_start = datetime.fromtimestamp(escrow.start_time())
            # date_time_start_formatted = date_time_start.strftime("%m/%d/%Y, %H:%M:%S")
            # print('Start date: ',date_time_start_formatted)
            # end_cliff = escrow.start_time() + x['cliff']
            # end_cliff_start = datetime.fromtimestamp(end_cliff)
            # end_cliff_formatted = end_cliff_start.strftime("%m/%d/%Y, %H:%M:%S")
            # print('Cliff ends date: ',end_cliff_formatted)
            # date_time_end = datetime.fromtimestamp(escrow.end_time())
            # date_time_end_formatted = date_time_end.strftime("%m/%d/%Y, %H:%M:%S")
            # print('End date: ',date_time_end_formatted)

            # print(f"progress {escrow.unclaimed() / escrow.total_locked():.3%}")
            # print("unclaimed", escrow.unclaimed().to("ether"))
