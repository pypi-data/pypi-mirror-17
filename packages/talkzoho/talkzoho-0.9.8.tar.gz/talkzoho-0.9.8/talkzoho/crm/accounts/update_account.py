from talkzoho.regions import US
from talkzoho.crm.update_record import update_record
from talkzoho.crm.accounts import MODULE, PRIMARY_KEY


async def update_account(record,
                         *,
                         auth_token=None,
                         region=US):
    return await update_record(
        MODULE,
        primary_key=PRIMARY_KEY,
        record=record,
        auth_token=auth_token,
        region=region)
