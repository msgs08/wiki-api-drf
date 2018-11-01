from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import ugettext as _
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        label=_("Password"),
        help_text=password_validation.password_validators_help_text_html(),
        write_only=True,
    )
    password2 = serializers.CharField(
        label=_("Password confirmation"),
        help_text=_("Enter the same password as before, for verification."),
        write_only=True,
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def create(self, validated_data):
        print('create :', validated_data)
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        password1 = attrs.pop('password1', None)
        password2 = attrs.pop('password2', None)

        if password1 is not None:
            if password1 != password2:
                raise serializers.ValidationError(
                    _('Passwords do not match.')
                )
            else:
                attrs['password'] = password1
            password_validation.validate_password(attrs['password'], self.instance)
        return attrs
