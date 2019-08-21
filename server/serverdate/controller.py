from datetime import datetime

from protocol import make_response


def server_date_controller(request):
    return make_response(request, 200, datetime.now().timestamp())