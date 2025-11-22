from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

from .models import UserProfile

signer = TimestampSigner()


def generate_email_token(email: str) -> str:
    """Generate a signed token for email verification."""
    return signer.sign(email)


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
