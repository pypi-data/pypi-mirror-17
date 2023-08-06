import os

from typing import Optional

from urllib.parse import urlencode

from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_decode

from talkzoho.regions import US
from talkzoho.utils import create_url

from talkzoho.crm import BASE_URL, API_PATH, SCOPE, ENVIRON_AUTH_TOKEN
from talkzoho.crm.utils import wrap_items, unwrap_items


async def update_record(module: str,
                        record: dict,
                        *,
                        primary_key: str,
                        auth_token: Optional[str]=None,
                        region: str=US,
                        trigger_workflow: bool=True):
    client     = AsyncHTTPClient()
    path       = API_PATH + '/' + module + '/updateRecords'
    endpoint   = create_url(BASE_URL, tld=region, path=path)

    id_        = record.pop(primary_key)
    xml_record = wrap_items(record, module_name=module)

    body = urlencode({
        'scope': SCOPE,
        'version': 2,
        'newFormat': 2,
        'duplicateCheck': 1,
        'wfTrigger': str(trigger_workflow).lower(),
        'id': id_,
        'xmlData': xml_record,
        'authtoken': auth_token or os.getenv(ENVIRON_AUTH_TOKEN)})

    response = await client.fetch(endpoint, method='POST', body=body)
    body     = json_decode(response.body.decode('utf-8'))

    return unwrap_items(body, single_item=True)['Id']
