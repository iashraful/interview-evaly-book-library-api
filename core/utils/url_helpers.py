def url_to_dict(url: str) -> dict:
    """
    This function do the url conversion to dictionary.
    Expected format:
    http://example.com?ref=auth&back_to=https://ashraful.dev
    """
    if not isinstance(url, str):
        raise ValueError(f'Expected string, got {type(url)}')
    _dict = {
        'params': []
    }
    base_url = url.split('?')[0]
    params = url.split('?')[1] if '?' in url else None
    _dict['base_url'] = base_url
    _params = _dict['params']
    if not params:
        return _dict
    for param in params.split('&'):
        key, value = param.split('=')
        _params.append({
            'key': key,
            'value': value
        })
    return _dict


def dict_to_url(url_dict: dict) -> str:
    """
        This function do the url conversion to dictionary.
        Expected format:
        {
            "base_url": "example.com",
            "params": [{
                "key": "actual key",
                "value": "actual value"
            }, {...}]
        }
        """
    if not isinstance(url_dict, dict):
        raise ValueError(f'Expected dictionary, got {type(url_dict)}')
    url = f'{url_dict["base_url"]}?'
    for param in url_dict['params']:
        url = f'{url}{param["key"]}={param["value"]}'
    return url


def add_param_to_url(url: str, param: dict) -> str:
    """
    This methods helps to add additional param on url
    url: should be string
    param: expected format {'key': 'a key', 'value': 'a value'}
    """
    url_dict = url_to_dict(url)
    url_dict['params'].append(param)
    return dict_to_url(url_dict)

def replace_base_url(url: str, new_url: str) -> str:
    url_dict = url_to_dict(url)
    url_dict['base_url'] = new_url
    return dict_to_url(url_dict)
