from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile
from .serializers import UserProfileSerializer, ChangePasswordSerializer, CustomTokenObtainPairSerializer
from .utils import send_verification_email, verify_email_token, extract_email_from_token


class UserProfileViewSet(mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action in ["create", "verify_email", "resend_verification_email"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_verification_email(user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"detail": "Account created. Check your email to verify your account."},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=False, methods=["get"], url_path="verify-email")
    def verify_email(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response({"detail": "Token missing."}, status=400)

        email = verify_email_token(token)
        if email:
            try:
                user = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                return Response({"detail": "User not found."}, status=404)

            if user.email_verified:
                return Response({"detail": "Email already verified.", "email": email}, status=200)

            user.email_verified = True
            user.save()

            return Response({"detail": "Email verified.", "email": email}, status=200)

        extracted_email = extract_email_from_token(token)
        if extracted_email:
            return Response({"detail": "Token expired.", "email": extracted_email}, status=410)

        return Response({"detail": "Invalid verification link."}, status=400)

    @action(detail=False, methods=["post"], url_path="resend-verification-email")
    def resend_verification_email(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required."}, status=400)

        try:
            user = UserProfile.objects.get(email=email)
            if not user.email_verified:
                send_verification_email(user)
        except UserProfile.DoesNotExist:
            pass

        return Response({"detail": "Verification email sent if the account exists."}, status=200)

    @action(detail=False, methods=["get"], url_path="me")
    def get_self_info(self, request):
        user = self.request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["put"], url_path="change-password")
    def change_password(self, request):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data, context={"user": user})
        if serializer.is_valid():
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]
            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
