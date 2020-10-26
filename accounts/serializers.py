from phonenumbers import is_valid_number, parse as phonenumbers_parse
from rest_framework import serializers, exceptions

from accounts.models import User


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'passcode')


class SignInRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    def validate(self, attrs):
        phone = attrs.get('username').replace(" ", "")
        if is_valid_number(phonenumbers_parse(phone, None)):
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                attrs['phone'] = phone
            else:
                if user.is_active:
                    attrs['user'] = user
                else:
                    msg = 'User is deactivated.'
                    raise exceptions.ValidationError(msg)
        else:
            msg = 'Must provide phonenumber in internation format'
            raise exceptions.ValidationError(msg)
        return attrs
