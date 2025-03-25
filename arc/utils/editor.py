import os
import subprocess
import tempfile


def get_editor_input(prompt: str | None = None) -> str:
    """Get input from user's default editor."""
    editor = os.environ.get("EDITOR", "vim")
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".md", delete=False) as temp:
        if prompt:
            temp.write(prompt)
        temp_path = temp.name
    subprocess.call([editor, temp_path])
    with open(temp_path) as f:
        content = f.read().strip()
    os.unlink(temp_path)
    return content


def create_tar(timestamp: str, directory: str) -> str:
    """Create a tar archive of a directory."""
    tar_name = f"message-{timestamp}.tar"
    subprocess.run(["tar", "-cvf", tar_name, directory], check=True)
    return tar_name
