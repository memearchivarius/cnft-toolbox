from random import getrandbits
from typing import Any, Dict, Optional

from aiogram.client.session import aiohttp
from pytoniq_core import Cell, begin_cell, Address, StateInit

ITEM_CODE = "b5ee9c7241020e010001dc000114ff00f4a413f4bcf2c80b0102016202030202ce04050009a11f9fe00502012006070201200c0d02cf0c8871c02497c0f83434c0c05c6c2497c0f83e903e900c7e800c5c75c87e800c7e800c1cea6d003c00812ce3850c1b088d148cb1c17cb865407e90350c0408fc00f801b4c7f4cfe08417f30f45148c2eb8c08c0d0d0d4d60840bf2c9a884aeb8c097c12103fcbc20080900113e910c30003cb8536002ac3210375e3240135135c705f2e191fa4021f001fa40d20031fa0020d749c200f2e2c4820afaf0801ba121945315a0a1de22d70b01c300209206a19136e220c2fff2e1922194102a375be30d0293303234e30d5502f0030a0b00727082108b77173505c8cbff5004cf1610248040708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb00007c821005138d91c85009cf16500bcf16712449145446a0708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb001047006a26f0018210d53276db103744006d71708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb00003b3b513434cffe900835d27080269fc07e90350c04090408f80c1c165b5b60001d00f232cfd633c58073c5b3327b552013b582a8"  # noqa


async def _fetch(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
    except (Exception,):
        return None


async def get_proof_params(base_url: str, owner_addr: str) -> Optional[Dict[str, Any]]:
    url = f"{base_url}/v1/address/{owner_addr}"
    return await _fetch(url)


async def is_claimed(is_testnet: bool, nft_addr: str) -> bool:
    base_url = "https://testnet.toncenter.com" if is_testnet else "https://toncenter.com"
    url = f"{base_url}/api/v2/getTokenData"
    params = {"address": nft_addr}

    response = await _fetch(url, params)
    return response is not None


def calculate_nft_item_address(collection_addr: str, index: int) -> Address:
    data = (
        begin_cell()
        .store_uint(index, 64)
        .store_address(collection_addr)
        .end_cell()
    )
    code = Cell.one_from_boc(ITEM_CODE)
    state_init = StateInit(code=code, data=data)

    return Address((0, state_init.serialize().hash))


def build_claim_body(index: int, proof_cell: str) -> Cell:
    return (
        begin_cell()
        .store_uint(0x13a3ca6, 32)
        .store_uint(getrandbits(64), 64)
        .store_uint(index, 256)
        .store_ref(Cell.one_from_boc(proof_cell))
        .end_cell()
    )
