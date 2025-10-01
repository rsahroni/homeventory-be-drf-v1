from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from allauth.account.adapter import get_adapter
from django.db import transaction
from django.contrib.auth import get_user_model


class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom serializer for user registration that includes first_name and last_name.
    """

    full_name = serializers.CharField(max_length=60, required=True)
    username = None  # Remove the username field

    def validate_email(self, email):
        """
        Use allauth's logic to check if the email is unique.
        This makes the validation explicit and prevents IntegrityError.
        """
        User = get_user_model()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                "A user is already registered with this e-mail address."
            )

        email = get_adapter().clean_email(email)
        # The clean_email method from allauth handles other validations (e.g., format).
        return email

    def validate_full_name(self, full_name):
        """
        Validate that the full_name contains at least one word.
        """
        if not full_name or not full_name.strip():
            raise ValidationError("This field may not be blank.")
        return full_name

    def custom_signup(self, request, user):
        """
        This method is called by dj-rest-auth's RegisterView after the user
        is initially created. We use it to parse and save the full_name.
        """
        full_name = self.validated_data.get("full_name", "").strip()
        name_parts = full_name.strip().split()

        if len(name_parts) == 1:
            user.first_name = name_parts[0]
            user.last_name = ""  # Explicitly set last_name to blank
        elif len(name_parts) > 1:
            user.last_name = name_parts.pop()
            user.first_name = " ".join(name_parts)

        user.save()
