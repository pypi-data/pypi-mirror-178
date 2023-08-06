import typing_extensions

from circle_sdk.apis.tags import TagValues
from circle_sdk.apis.tags.payments_api import PaymentsApi
from circle_sdk.apis.tags.on_chain_payments_api import OnChainPaymentsApi
from circle_sdk.apis.tags.cards_api import CardsApi
from circle_sdk.apis.tags.wires_api import WiresApi
from circle_sdk.apis.tags.ach_api import ACHApi
from circle_sdk.apis.tags.sepa_api import SEPAApi
from circle_sdk.apis.tags.settlements_api import SettlementsApi
from circle_sdk.apis.tags.chargebacks_api import ChargebacksApi
from circle_sdk.apis.tags.reversals_api import ReversalsApi
from circle_sdk.apis.tags.balances_api import BalancesApi
from circle_sdk.apis.tags.health_api import HealthApi
from circle_sdk.apis.tags.management_api import ManagementApi
from circle_sdk.apis.tags.encryption_api import EncryptionApi
from circle_sdk.apis.tags.subscriptions_api import SubscriptionsApi
from circle_sdk.apis.tags.stablecoins_api import StablecoinsApi
from circle_sdk.apis.tags.channels_api import ChannelsApi
from circle_sdk.apis.tags.wallets_api import WalletsApi
from circle_sdk.apis.tags.transfers_api import TransfersApi
from circle_sdk.apis.tags.payouts_api import PayoutsApi
from circle_sdk.apis.tags.on_chain_payouts_api import OnChainPayoutsApi
from circle_sdk.apis.tags.returns_api import ReturnsApi
from circle_sdk.apis.tags.payment_intents_api import PaymentIntentsApi
from circle_sdk.apis.tags.address_book_api import AddressBookApi
from circle_sdk.apis.tags.addresses_api import AddressesApi
from circle_sdk.apis.tags.deposits_api import DepositsApi
from circle_sdk.apis.tags.sen_api import SENApi
from circle_sdk.apis.tags.signet_api import SignetApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.PAYMENTS: PaymentsApi,
        TagValues.ONCHAIN_PAYMENTS: OnChainPaymentsApi,
        TagValues.CARDS: CardsApi,
        TagValues.WIRES: WiresApi,
        TagValues.ACH: ACHApi,
        TagValues.SEPA: SEPAApi,
        TagValues.SETTLEMENTS: SettlementsApi,
        TagValues.CHARGEBACKS: ChargebacksApi,
        TagValues.REVERSALS: ReversalsApi,
        TagValues.BALANCES: BalancesApi,
        TagValues.HEALTH: HealthApi,
        TagValues.MANAGEMENT: ManagementApi,
        TagValues.ENCRYPTION: EncryptionApi,
        TagValues.SUBSCRIPTIONS: SubscriptionsApi,
        TagValues.STABLECOINS: StablecoinsApi,
        TagValues.CHANNELS: ChannelsApi,
        TagValues.WALLETS: WalletsApi,
        TagValues.TRANSFERS: TransfersApi,
        TagValues.PAYOUTS: PayoutsApi,
        TagValues.ONCHAIN_PAYOUTS: OnChainPayoutsApi,
        TagValues.RETURNS: ReturnsApi,
        TagValues.PAYMENT_INTENTS: PaymentIntentsApi,
        TagValues.ADDRESS_BOOK: AddressBookApi,
        TagValues.ADDRESSES: AddressesApi,
        TagValues.DEPOSITS: DepositsApi,
        TagValues.SEN: SENApi,
        TagValues.SIGNET: SignetApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.PAYMENTS: PaymentsApi,
        TagValues.ONCHAIN_PAYMENTS: OnChainPaymentsApi,
        TagValues.CARDS: CardsApi,
        TagValues.WIRES: WiresApi,
        TagValues.ACH: ACHApi,
        TagValues.SEPA: SEPAApi,
        TagValues.SETTLEMENTS: SettlementsApi,
        TagValues.CHARGEBACKS: ChargebacksApi,
        TagValues.REVERSALS: ReversalsApi,
        TagValues.BALANCES: BalancesApi,
        TagValues.HEALTH: HealthApi,
        TagValues.MANAGEMENT: ManagementApi,
        TagValues.ENCRYPTION: EncryptionApi,
        TagValues.SUBSCRIPTIONS: SubscriptionsApi,
        TagValues.STABLECOINS: StablecoinsApi,
        TagValues.CHANNELS: ChannelsApi,
        TagValues.WALLETS: WalletsApi,
        TagValues.TRANSFERS: TransfersApi,
        TagValues.PAYOUTS: PayoutsApi,
        TagValues.ONCHAIN_PAYOUTS: OnChainPayoutsApi,
        TagValues.RETURNS: ReturnsApi,
        TagValues.PAYMENT_INTENTS: PaymentIntentsApi,
        TagValues.ADDRESS_BOOK: AddressBookApi,
        TagValues.ADDRESSES: AddressesApi,
        TagValues.DEPOSITS: DepositsApi,
        TagValues.SEN: SENApi,
        TagValues.SIGNET: SignetApi,
    }
)
