from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton as Button
from aiogram.types import InlineKeyboardMarkup as Markup
from aiogram.types import Message, CallbackQuery
from aiogram.types import User
from aiogram.utils.markdown import hbold, hlink, hide_link
from aiogram_tonconnect import ATCManager
from aiogram_tonconnect.tonconnect.models import (
    ConnectWalletCallbacks,
    SendTransactionCallbacks,
)
from tonutils.tonconnect.models import Transaction

from .config import Config
from .utils import get_proof_params, build_claim_body, calculate_nft_item_address, is_claimed

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)


class UserState(StatesGroup):
    CONNECT_WALLET = State()
    MAIN_MENU = State()
    TRANSACTION_SENT = State()


async def connect_wallet_window(atc_manager: ATCManager) -> None:
    event_from_user: User = atc_manager.middleware_data.get("event_from_user")

    text = hide_link("https://telegra.ph//file/aaba319da09f60e6def03.jpg") + (
        f"👋 Hi {hbold(event_from_user.full_name)}!\n\n"
        "Please, connect your wallet to access features."
    )
    reply_markup = Markup(
        inline_keyboard=[
            [Button(text="Connect Wallet", callback_data="connect_wallet")]
        ]
    )

    await atc_manager._send_message(text, reply_markup=reply_markup)  # noqa
    await atc_manager.state.set_state(UserState.CONNECT_WALLET)


async def main_menu_window(atc_manager: ATCManager) -> None:
    config: Config = atc_manager.middleware_data.get("config")
    wallet_address = atc_manager.connector.account.address.to_str(is_bounceable=False)

    url = (
        f"https://testnet.tonviewer.com/{wallet_address}"
        if config.IS_TESTNET else
        f"https://tonviewer.com/{wallet_address}"
    )
    title = f"{wallet_address[:4]}...{wallet_address[-4:]}"
    wallet_link = hlink(title, url)

    text = hide_link("https://telegra.ph//file/db9c5c3febe75811e41af.jpg") + (
        f"🤖 {hbold('Welcome to the NFT Claim Bot!')}\n\n"
        "You can now request your NFT claim.\n\n"
        f"{hbold('Connected to:')} {wallet_link}"
    )

    reply_markup = Markup(
        inline_keyboard=[
            [Button(text="Request NFT Claim", callback_data="claim_nft")],
            [Button(text="Disconnect Wallet", callback_data="disconnect_wallet")],
        ]
    )

    await atc_manager._send_message(text, reply_markup=reply_markup)  # noqa
    await atc_manager.state.set_state(UserState.MAIN_MENU)


async def transaction_sent_window(atc_manager: ATCManager) -> None:
    text = hide_link("https://telegra.ph//file/aaba319da09f60e6def03.jpg") + (
        f"🎉 {hbold('Request to claim NFT has been sent!')}\n\n"
        "Please, wait for a few minutes."
    )
    reply_markup = Markup(
        inline_keyboard=[
            [Button(text="Main Menu", callback_data="main_menu")]
        ]
    )

    await atc_manager._send_message(text, reply_markup=reply_markup)  # noqa
    await atc_manager.state.set_state(UserState.TRANSACTION_SENT)


@router.message(CommandStart())
async def start_command(message: Message, atc_manager: ATCManager) -> None:
    await atc_manager.tonconnect.init_connector(message.from_user.id)

    if atc_manager.connector.connected:
        await main_menu_window(atc_manager)
    else:
        await atc_manager.update_interfaces_language(language_code="en")
        await atc_manager.state.update_data(language_code="en")
        await connect_wallet_window(atc_manager)

    await message.delete()


@router.callback_query(UserState.CONNECT_WALLET)
async def connect_wallet_callback_handler(call: CallbackQuery, atc_manager: ATCManager) -> None:
    if call.data == "connect_wallet":
        callbacks = ConnectWalletCallbacks(
            before_callback=connect_wallet_window,
            after_callback=main_menu_window,
        )
        await atc_manager.connect_wallet(callbacks)

    await call.answer()


@router.callback_query(UserState.MAIN_MENU)
async def callback_query_handler(call: CallbackQuery, atc_manager: ATCManager) -> None:
    await atc_manager.tonconnect.init_connector(call.from_user.id)

    config: Config = atc_manager.middleware_data.get("config")
    wallet_address = atc_manager.connector.account.address.to_str(is_bounceable=False)

    if call.data == "claim_nft":
        await atc_manager._send_message("⏳")  # noqa
        proof_params = await get_proof_params(config.API_BASE_URL, wallet_address)

        if proof_params is None:
            text = "NFT claim request failed! You are not on the whitelist."
            await call.answer(text, show_alert=True)
            await main_menu_window(atc_manager)
        else:
            proof_cell = proof_params["proof_cell"]
            item_index = int(proof_params["item"]["index"])
            item_address = calculate_nft_item_address(config.COLLECTION_ADDRESS, item_index)

            if await is_claimed(config.IS_TESTNET, item_address.to_str()):
                text = "NFT is already claimed!"
                await call.answer(text, show_alert=True)
                await main_menu_window(atc_manager)
            else:
                text = (
                    "Congratulations! You are on the whitelist. "
                    "To claim NFT confirm transaction on your wallet."
                )
                await call.answer(text, show_alert=True)

                transaction = Transaction(
                    messages=[
                        Transaction.create_message(
                            destination=config.COLLECTION_ADDRESS,
                            body=build_claim_body(item_index, proof_cell),
                            amount=0.085,
                        )
                    ]
                )
                callbacks = SendTransactionCallbacks(
                    before_callback=main_menu_window,
                    after_callback=transaction_sent_window,
                )
                await atc_manager.send_transaction(transaction, callbacks)

    elif call.data == "disconnect_wallet":
        await atc_manager.disconnect_wallet()
        await connect_wallet_window(atc_manager)

    await call.answer()


@router.callback_query(UserState.TRANSACTION_SENT)
async def transaction_sent_callback_handler(call: CallbackQuery, atc_manager: ATCManager) -> None:
    await atc_manager.tonconnect.init_connector(call.from_user.id)

    if call.data == "main_menu":
        await main_menu_window(atc_manager)

    await call.answer()


@router.message()
async def default_message_handler(message: Message) -> None:
    await message.delete()
