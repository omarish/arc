"""Core functionality for handling letter operations."""

import os
import re
from datetime import datetime

from ..crypto.encrypt import encrypt_data, generate_keypair
from ..email.sender import send_email
from ..utils.editor import create_tar, get_editor_input


class LetterSender:
    def __init__(self, key_dir: str = "private_keys", gmail_password: str | None = None):
        self.key_dir = key_dir
        self.gmail_password = gmail_password or os.environ.get("GMAIL_APP_PASSWORD")
        if not self.gmail_password:
            raise ValueError(
                "Gmail app password is required. Set GMAIL_APP_PASSWORD environment variable or pass it directly."
            )

    def _validate_email(self, email: str) -> bool:
        """Validate email address format."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def _get_key_path(self, email: str, timestamp: str) -> str:
        """Get the path where the key should be stored."""
        # Create sanitized directory name from email
        email_dir = email.replace("@", "_at_").replace(".", "_dot_")
        key_path = os.path.join(self.key_dir, email_dir)
        os.makedirs(key_path, exist_ok=True)
        return os.path.join(key_path, f"{timestamp}.pem")

    def _get_subject(self, provided_subject: str | None = None) -> str:
        """Get the email subject, either from provided value or user input."""
        if provided_subject:
            return provided_subject

        subject = get_editor_input("Enter subject line:\n# Lines starting with # will be ignored\n")
        subject = "\n".join(
            line for line in subject.splitlines() if line and not line.startswith("#")
        ).strip()
        if not subject:
            raise ValueError("Subject cannot be empty")
        return subject

    def _prepare_input_data(self, input_path: str, timestamp: str) -> tuple[bytes, str, list[str]]:
        """Prepare input data for encryption. Returns (data, input_filename, cleanup_files)."""
        if os.path.isdir(input_path):
            tar_name = create_tar(timestamp, input_path)
            with open(tar_name, "rb") as f:
                data = f.read()
            return data, tar_name, [tar_name]
        elif os.path.isfile(input_path):
            with open(input_path, "rb") as f:
                data = f.read()
            return data, input_path, []
        else:
            raise ValueError(f"{input_path} is not a valid file or directory")

    def _process_recipient(
        self, email: str, data: bytes, input_filename: str, timestamp: str, subject: str
    ) -> None:
        """Process a single recipient's letter."""
        if not self._validate_email(email):
            raise ValueError(f"Invalid email address: {email}")

        # Generate keypair with email-based directory structure
        key_path = self._get_key_path(email, timestamp)
        private_key, public_key = generate_keypair(timestamp, email, key_path)

        # Encrypt data
        enc_name = encrypt_data(data, public_key, timestamp, email)

        # Rename to follow file.ext.enc pattern
        base_name = os.path.basename(input_filename)
        new_enc_name = f"{base_name}.enc"
        os.rename(enc_name, new_enc_name)

        try:
            # Send email
            send_email(email, subject, new_enc_name, self.gmail_password)
        finally:
            # Clean up encrypted file
            if os.path.exists(new_enc_name):
                os.remove(new_enc_name)

    def send_letter(
        self, input_path: str, recipients: list[str], subject: str | None = None
    ) -> None:
        """
        Send an encrypted letter to specified recipients.

        Args:
            input_path: Path to file or directory to encrypt and send
            recipients: List of recipient email addresses
            subject: Optional email subject (will prompt if not provided)
        """
        if not recipients:
            raise ValueError("Must specify at least one recipient")

        # Get timestamp for unique key generation
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")

        # Get subject
        subject = self._get_subject(subject)

        # Prepare input data
        data, input_filename, cleanup_files = self._prepare_input_data(input_path, timestamp)

        try:
            # Process each recipient
            for recipient in recipients:
                self._process_recipient(recipient, data, input_filename, timestamp, subject)
        finally:
            # Clean up temporary files
            for file in cleanup_files:
                if os.path.exists(file):
                    os.remove(file)
