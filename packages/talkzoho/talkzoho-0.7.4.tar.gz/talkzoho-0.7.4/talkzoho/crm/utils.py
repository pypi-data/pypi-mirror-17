from tornado.web import HTTPError


def select_columns(resource, columns):
    return resource.lower() + '(' + ','.join(columns) + ')' if columns else ''


def value_to_xml_data(value, *, is_primary_field: bool=False):
    if is_primary_field:
        return str(value)
    else:
        return '<![CDATA[{}]]>'.format(value)


def record_to_xml_data(record: dict, *, primary_field: str):
    record = {k: value_to_xml_data(v, is_primary_field=(k == primary_field))
              for k, v in record.items()}
    lines  = ['<FL val="{}">{}</FL>'.format(k, v)
              for k, v in record.items()]

    return ''.join(lines)


def wrap_items(items, *, module_name: str, primary_field: str):
    if type(items) is not list:
        items = [items]

    rows = ['<row no="{}">{}</row>'.format(index + 1, record_to_xml_data(item, primary_field=primary_field))  # noqa
            for index, item in enumerate(items)]

    return '<{module_name}>{rows}</{module_name}>'.format(
        module_name=module_name,
        rows=''.join(rows))


def unwrap_items(response, single_item=False):
    try:
        result   = response['response']['result']

        if len(result) == 1:
            # Don't know the resource name but should be the only key
            resource = list(result.values())[0]
            rows     = resource['row']
        elif len(result) == 2:
            # On update message returns two keys message and record
            single_item = True
            rows        = result['recorddetail']
        else:
            raise ValueError('Unexpected looking response.')

        # wrap single resource results in array
        items = rows if isinstance(rows, list) else [rows]

        if single_item and len(items) != 1:
            ValueError('More then one resource was returned.')

        items = [translate_item(i) for i in items]
        return items[0] if single_item else items
    except (AssertionError, KeyError):
        unwrap_error(response)


def unwrap_error(zoho_error):
    try:
        response   = zoho_error['response']
        filtered   = {key: value for key, value in response.items() if key.lower() != 'uri'}  # noqa

        # Dont know the error name but should ony be one key left
        assert len(filtered) == 1
        _, error      = filtered.popitem()
        code, message = error['code'], error['message']

        status_code = http_status_code(zoho_code=code)
        raise HTTPError(status_code, reason=message)
    except (AssertionError, KeyError, IndexError):
        raise ValueError("Couldn't parse zoho result")


def http_status_code(*, zoho_code):  # pragma: no cover
    zoho_code = str(zoho_code)

    if zoho_code in ["4000", "4401", "4600", "4831", "4832", "4835", "4101", "4420"]:  # noqa
        return 400  # bad request
    elif zoho_code in ["4501", "4834"]:
        return 401  # unauthorised
    elif zoho_code in ["4502", "4890"]:
        return 402  # payment required
    elif zoho_code in ["4487", "4001", "401", "401.1", "401.2", "401.3"]:
        return 403  # forbidden
    elif zoho_code in ["4102", "4103", "4422"]:
        return 404  # not found
    elif zoho_code in []:
        return 405  # method not allowed
    elif zoho_code in ["4807"]:
        return 413  # payload too large
    elif zoho_code in ["4424"]:
        return 415  # payload too large
    elif zoho_code in ["4101", "4809"]:
        return 423  # locked
    elif zoho_code in ["4820", "4421", "4423"]:
        return 429  # too many requests
    else:
        return 500  # internal server error


def translate_item(item):
    fields = item.get('fl', item.get('FL'))
    fields = fields if isinstance(fields, list) else [fields]

    def nullify(value):
        return None if value == 'null' else value

    return {kwarg['val']: nullify(kwarg['content']) for kwarg in fields}
