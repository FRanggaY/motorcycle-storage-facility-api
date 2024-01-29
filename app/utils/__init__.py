async def validate_file_content_type(content_type: str, allowed_content_types: tuple):
    if content_type.lower() not in allowed_content_types:
        raise ValueError(f"Invalid file content type. Only {', '.join(allowed_content_types)} files are allowed.")