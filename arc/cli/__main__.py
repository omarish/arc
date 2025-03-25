"""Command-line interface for Arc."""

import argparse
import os
import sys

from ..core.letters import LetterSender


def validate_input_path(path: str) -> None:
    """Validate that the input path exists."""
    if not os.path.exists(path):
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)


def send_letter(args: argparse.Namespace) -> None:
    """Handle the send command for the CLI."""
    validate_input_path(args.input)

    try:
        # Create sender and send letter
        sender = LetterSender(key_dir=args.key_dir)
        sender.send_letter(input_path=args.input, recipients=args.recipient, subject=args.subject)
        print(f"✨ Successfully sent letter to {len(args.recipient)} recipient(s)")

        # Print key locations
        print("\nPrivate keys stored in:")
        for email in args.recipient:
            email_dir = email.replace("@", "_at_").replace(".", "_dot_")
            key_dir = os.path.join(args.key_dir, email_dir)
            print(f"  • {key_dir}/")

    except ValueError as e:
        print(f"Error: {e!s}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e!s}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Send encrypted letters to recipients",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Send to a single recipient:
    %(prog)s send --recipient daughter@example.com letter.md

  Send to multiple recipients:
    %(prog)s send --recipient daughter1@example.com --recipient daughter2@example.com letter.md

  Send with a subject:
    %(prog)s send --recipient daughter@example.com --subject "Happy Birthday" letter.md

  Send a folder (will be automatically archived):
    %(prog)s send --recipient daughter@example.com folder/
""",
    )

    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # Send command
    send_parser = subparsers.add_parser("send", help="Send an encrypted letter")
    send_parser.add_argument(
        "--recipient",
        action="append",
        required=True,
        metavar="EMAIL",
        help="Email address of recipient. Can be specified multiple times for multiple recipients.",
    )
    send_parser.add_argument("--subject", help="Email subject line (opens editor if not specified)")
    send_parser.add_argument(
        "--key-dir",
        default="private_keys",
        help="Directory for storing private keys (default: private_keys)",
    )
    send_parser.add_argument("input", help="File or directory to encrypt and send")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    if args.action == "send":
        send_letter(args)


if __name__ == "__main__":
    main()
