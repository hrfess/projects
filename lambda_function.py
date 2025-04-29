import json
import openai

openai.api_key = "sk-proj-4EYdWD2k7qp4FJiEcicr0tinhMfrORCMWVGcn3M_GdSlbWUrHbpSJAA"

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        user_messages = body.get("messages", [])

        # Prepend system message to guide the assistant's personality
        system_msg = {
            "role": "system",
            "content": (
                "You're ChatBFF, the user's hilarious, supportive best friend. "
                "Always reply like you're texting a close buddy: super casual, funny, encouraging, and full of personality. "
                "Use slang, emojis when it fits, and keep it fun and informal. Be their hype-person. 🎉"
            )
        }

        # Combine system and user messages
        messages = [system_msg] + user_messages

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.9
        )

        reply = response["choices"][0]["message"]["content"]

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"reply": reply})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
