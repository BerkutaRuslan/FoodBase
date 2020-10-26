from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from accounts.serializers import SignInRequestSerializer, UserPhoneSerializer, SignInVerifySerializer, \
    UserFullSerializer
from accounts.utils import send_sms_code


class SignInRequestView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignInRequestSerializer

    def post(self, request):
        request_time = timezone.now()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.validated_data['user']
            except KeyError:
                user = serializer.save()

            if user.passcode_timer:
                if request_time < user.passcode_timer:
                    wait_for = (user.passcode_timer - request_time).seconds
                    return Response({"error": f"Wait {wait_for} seconds and try again"},
                                    status=status.HTTP_400_BAD_REQUEST)

            # if user is new or passcode time has passed
            code = send_sms_code(user.phone)
            if code:
                user.passcode = code
                user.passcode_timer = timezone.now() + timezone.timedelta(minutes=1)
                user.save()

                user_serializer = UserPhoneSerializer(user)

                return Response(user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Message was not delivered to user"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SignInVerifyView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignInVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user.first_name != "":
                is_new_user = False
                user_serializer = UserFullSerializer(user)
            else:
                is_new_user = True
                user_serializer = UserPhoneSerializer(user)

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'is_new_user': is_new_user, 'user': user_serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
