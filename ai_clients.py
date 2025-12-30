#try:
 #   from local_secrets import OPENAI_API_KEY
#except ImportError:
 #   OPENAI_API_KEY = None

import streamlit as st
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
from openai import OpenAI


def call_chatgpt(prompt: str) -> str:
    if not OPENAI_API_KEY:
        return (
            "❌ **API key not found.**\n\n"
            "Please add your OpenAI API key in `secrets.py`."
        )

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AWS Support Engineer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception as e:
        return (
            "⚠️ **AI service error occurred.**\n\n"
            f"Details: `{str(e)}`"
        )
