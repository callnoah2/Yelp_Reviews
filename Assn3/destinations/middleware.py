from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib.auth.models import User

class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, req):
        # Step 1: Read the session_token out of the cookie
        session_token = req.COOKIES.get(settings.SESSION_COOKIE_NAME)

        # Step 2: Find the session by its token
        try:
            session = Session.objects.get(session_key=session_token)

            # Step 4: Get the user from the session and attach it to the request.
            user_id = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=user_id)
            req.user = user

        except Session.DoesNotExist:
            pass

        # Step 5: Handle cases where the user is not logged in
        login_required_paths = [reverse('sessions'), reverse('newSessions')]  # Add other paths that don't require login

        if not req.user and req.path not in login_required_paths:
            return redirect(reverse('newSessions'))

        res = self.get_response(req)
        return res