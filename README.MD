This was built in order to demonstrate how a proxy is able to make a contract upgradeable. 

    1. deploy_and_upgrade.py will deploy the proxy contract and deploy the box contract on it.
    2. The script will call the store function giving a value of 1.
    3. The script will then upgrade the contract to BoxV2 and call the increment function.

In the case of a succesffull deployment and upgrade, the value will be incremented from 1 to 2.

