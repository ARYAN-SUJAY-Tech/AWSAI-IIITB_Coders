def format_output(ai_text: str) -> str:
    if not ai_text or not ai_text.strip():
        return "⚠️ No response generated."

    return ai_text
