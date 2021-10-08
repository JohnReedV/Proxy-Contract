from scripts.help_script import get_account, encode_function_data, upgrade
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, Contract, BoxV2


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": account})

    proxy_admin = ProxyAdmin.deploy({"from": account})

    # initializer == constructor for proxies
    # initializer = box.store, 1
    # box_encoded_initializer_function = encode_function_data(initializer)

    box_encoded_initializer_function = encode_function_data()

    # deploy on proxy
    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin.address, box_encoded_initializer_function, {
            "from": account, "gas_limit": 1000000}
    )
    print(f"Proxy deployed to {proxy}")

    # call proxy not box || proxy points to box
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    print(proxy_box.retrieve())

    box_v2 = BoxV2.deploy({"from": account})
    upgrade_txn = upgrade(account, proxy, box_v2.address,
                          proxy_admin_contract=proxy_admin)
    upgrade_txn.wait(1)

    # redefine for v2
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    # call new function
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())
