from talkzoho.regions import US
from talkzoho.crm.insert_module import insert_module
from talkzoho.crm.leads import MODULE


async def insert_lead(record,
                           *,
                           auth_token=None,
                           region=US):
    return await insert_module(
        MODULE,
        record=record,
        auth_token=auth_token,
        region=region)
