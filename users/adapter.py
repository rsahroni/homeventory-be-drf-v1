from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to prevent username from being generated
    during social account signup.
    """

    def populate_username(self, request, user):
        """Set username to None as it's not used."""
        user.username = None
