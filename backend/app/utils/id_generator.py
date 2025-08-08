import uuid


def generate_unique_id(prefix: str = "img") -> str:
    """
    Generate a short, URL-friendly ID.
    Example: 'img_a8b1c9d2'
    """
    unique_part = uuid.uuid4().hex[:8]  # lowercase, no hyphens
    return f"{prefix}_{unique_part}"
