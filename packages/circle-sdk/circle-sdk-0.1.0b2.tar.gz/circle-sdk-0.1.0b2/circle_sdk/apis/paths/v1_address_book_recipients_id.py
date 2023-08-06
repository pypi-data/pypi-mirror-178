from circle_sdk.paths.v1_address_book_recipients_id.get import ApiForget
from circle_sdk.paths.v1_address_book_recipients_id.delete import ApiFordelete
from circle_sdk.paths.v1_address_book_recipients_id.patch import ApiForpatch


class V1AddressBookRecipientsId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
