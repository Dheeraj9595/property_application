import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from groq import Groq

# Initialize Groq client
client = Groq(api_key="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")


# Define the system prompt
SYSTEM_PROMPT = ("You are a real estate assistant. Answer questions about property buying and selling."
                 "You are a concise assistant. "
                 "Always answer in MAX 150 characters. "
                 "Use short bullet points or highlighted key points only."
                 "If someone ask property near indore suggest him/her 1. khandwa road properties are better and value for money 2. Super corridor road")


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": SYSTEM_PROMPT},  # System prompt
                    {"role": "user", "content": user_message}],
                model="llama-3.1-8b-instant",
            )

            bot_reply = chat_completion.choices[0].message.content
            # breakpoint()
            return JsonResponse({"response": bot_reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

#export GROQ_API_KEY="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"
from django.shortcuts import render

def chatbot_page(request):
    return render(request, 'chatbot.html')
