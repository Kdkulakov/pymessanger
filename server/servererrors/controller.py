from protocol import make_response

from decorators import login_required


@login_required
def server_error_controller(request):
    raise Exception('Server error message')
