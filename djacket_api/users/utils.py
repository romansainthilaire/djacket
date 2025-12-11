import secrets
import string

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

from .models import UserProfile

signer = TimestampSigner()


def generate_random_password(length: int = 20) -> str:
    """Generate a secure random password."""
    characters = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits
    )
    return "".join(secrets.choice(characters) for _ in range(length))


def generate_email_token(email: str) -> str:
    """Generate a signed token for email verification."""
    token = signer.sign(email)
    return token


def verify_email_token(token: str, max_age=60 * 60 * 24) -> str | None:  # 24h
    """Verify the signed email token and return the email if valid."""
    try:
        email = signer.unsign(token, max_age=max_age)
        return email
    except (BadSignature, SignatureExpired):
        return None


def extract_email_from_token(token: str) -> str | None:
    """
    Extract the email from a TimestampSigner generated token.
    Token format: <email>:<timestamp>:<signature>
    """
    try:
        email, _, _ = token.rsplit(":", 2)
        return email
    except ValueError:
        return None


def send_verification_email(user: UserProfile):
    """Send a verification email with a signed token."""
    token = generate_email_token(user.email)
    verification_link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    send_mail(
        subject="DJACKET - Vérification de votre adresse e-mail",
        message=f"Cliquer sur le lien pour vérifier votre adresse e-mail : {verification_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )
    user.email_verification_sent_at = timezone.now()
    user.save()


def send_temporary_password_email(user: UserProfile, password: string):
    """Send an email with a temporary password."""
    send_mail(
        subject="DJACKET - Réinitialisation de votre mot de passe",
        message=f"Votre nouveau mot de passe est : {password}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )
    user.temporary_password_sent_at = timezone.now()
    user.save()
