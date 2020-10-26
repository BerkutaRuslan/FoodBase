from phonenumbers import is_valid_number, parse as phonenumbers_parse
from rest_framework import serializers, exceptions

from accounts.models import User


class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'photo', 'address', 'balance']


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


class SignInVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    passcode = serializers.CharField()

    class Meta:
        model = User
        fields = ['phone', 'passcode']

    def validate(self, attrs):
        helper = {
            "phone": "Phone is required",
            "passcode": "Passcode is required"
        }
        for key, value in helper.items():
            if not attrs.get(key, None):
                raise exceptions.ValidationError(value)

        phone = attrs.get('phone').replace(" ", "")
        passcode = attrs.get('passcode')
        if is_valid_number(phonenumbers_parse(phone, None)):
            if len(passcode) == 4 and passcode.isdecimal():
                try:
                    user = User.objects.get(phone=phone)
                except User.DoesNotExist:
                    msg = 'User with provided phone does not exist'
                    raise exceptions.ValidationError(msg)
                else:
                    if passcode == user.passcode:
                        attrs['user'] = user
                        return attrs
                    else:
                        msg = 'Incorrect passcode.'
                        raise exceptions.ValidationError(msg)
            else:
                msg = 'Passcode must be 4-digit number.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Must provide phonenumber in international format.'
            raise exceptions.ValidationError(msg)
