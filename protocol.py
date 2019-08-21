def validate_request(raw):
    if 'action' in raw and 'time' in raw:
        return True
    return False


def make_response(request, code, data=None):
    return {
        'action': request.get('action'),
        'time': request.get('time'),
        'data': data,
        'code': code,
    }