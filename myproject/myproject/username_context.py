from django.contrib.auth.decorators import login_required

def user_info(request):
    if request.user.is_authenticated:
        return {'username': request.user.username}
    return {}
