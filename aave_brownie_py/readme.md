1. Swap our ETH for WETH
2. Deposit some ETH into Aave
3. Borrow some asset with the ETH collateral
    1. Sell that borrowed asset. (Short selling)
4. Repay everything back


Testing:
Integration test: Kovan
Unit tests: Mainnet-fork
    Note: If you're not using oracles and you don't need to mock responses, you can use mainnet-forking for uint tests.