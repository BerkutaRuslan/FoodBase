from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from FoodBase import settings
from FoodBase.utils import send_email
from accounts.models import ResetKey
from accounts.serializers import SignInRequestSerializer, UserPhoneSerializer, SignInVerifySerializer, \
    UserFullSerializer, UserPhotoSerializer, ForgotPasswordSerializer
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


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = UserFullSerializer(instance=request.user).data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserFullSerializer(data=request.data, instance=request.user, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserFullSerializer(user).data, status=status.HTTP_200_OK)
        else:
            raise ValidationError(serializer.errors)


class UpdatePhotoView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]

    def put(self, request):
        photo_obj = request.data['file']
        user = request.user
        try:
            user.photo = photo_obj
            user.save()
        except:
            return Response({'error': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(UserPhotoSerializer(user).data, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            reset_key = ResetKey.objects.create(user=user)
            reset_key.save()

            reset_password_url = f'{settings.HOST}/accounts/reset-password?key={reset_key.reset_key}'
            send_email(subject="Reset Password", user=user.email, template='reset-password.html',
                       from_email=settings.EMAIL_FROM_SENDER,
                       content={'user_name': f'{user.first_name} {user.last_name}', 'reset_url': reset_password_url})
            return Response({'message': 'Reset link was sent successfully, check your mail box',
                            'reset_key': reset_key.reset_key}, status=status.HTTP_200_OK)
