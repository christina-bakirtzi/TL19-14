def url_for(path):
    return '/energy/api' + path


def auth_header(token):
    return {
        'X-OBSERVATORY-AUTH': token
    }

def valid_response(real_data_list, json):
    for real_data in real_data_list:
        assert  real_data==json
