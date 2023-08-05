# This module will not be imported unless manually imported
from typing import Dict

import brownie.network.account
from .hacked_signing import fit_to_conflux

class LocalAccount(brownie.network.account.LocalAccount):
    def _transact(self, tx: Dict, allow_revert: bool) -> bytes:
        from brownie.network.web3 import web3
        from brownie._config import CONFIG
        if allow_revert is None:
            allow_revert = bool(CONFIG.network_type == "development")
        if not allow_revert:
            self._check_for_revert(tx)
        tx["chainId"] = hex(web3.chain_id)
        if isinstance(tx["data"], bytes):
            tx["data"] = tx["data"].hex()
        if isinstance(tx["nonce"], int):
            tx["nonce"] = hex(tx["nonce"])
        if isinstance(tx["value"], int):
            tx["value"] = hex(tx["value"])
        
        tx = fit_to_conflux(web3, tx)
        
        signed_tx = self._acct.sign_transaction(tx).rawTransaction  # type: ignore
        return web3.eth.send_raw_transaction(signed_tx)

brownie.network.account.LocalAccount = LocalAccount
