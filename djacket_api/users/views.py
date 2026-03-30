from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile
from .serializers import UserProfileSerializer, ChangePasswordSerializer, CustomTokenObtainPairSerializer
from .utils import (
    generate_random_password,
    send_verification_email,
    send_temporary_password_email,
    verify_email_token,
    extract_email_from_token
)


class UserProfileViewSet(mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action in [
            "create",
            "verify_email",
            "resend_verification_email",
            "reset_password"
        ]:
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
            return Response({"detail": "Token missing."}, status=status.HTTP_400_BAD_REQUEST)

        email = verify_email_token(token)
        if email:
            try:
                user = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            if user.email_verified:
                return Response({"detail": "Email already verified.", "email": email}, status=status.HTTP_200_OK)

            user.email_verified = True
            user.save()

            return Response({"detail": "Email verified.", "email": email}, status=status.HTTP_200_OK)

        extracted_email = extract_email_from_token(token)
        if extracted_email:
            return Response(
                {"detail": "Token invalid or expired.", "email": extracted_email},
                status=status.HTTP_410_GONE
            )

        return Response({"detail": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="resend-verification-email")
    def resend_verification_email(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserProfile.objects.get(email=email)
            if not user.email_verified:
                send_verification_email(user)
        except UserProfile.DoesNotExist:
            pass

        return Response({"detail": "Verification email sent if the account exists."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="me")
    def get_self_info(self, request):
        user = self.request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="reset-password")
    def reset_password(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = UserProfile.objects.filter(email=email).first()

        if user:
            new_password = generate_random_password()
            user.set_password(new_password)
            user.must_change_password = True
            user.save()
            send_temporary_password_email(user, new_password)

        return Response({"detail": "Temporary password sent if the account exists."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["put"], url_path="change-password")
    def change_password(self, request):
        user: UserProfile = self.request.user
        serializer = ChangePasswordSerializer(data=request.data, context={"user": user})
        if serializer.is_valid():
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]
            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.must_change_password = False
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
