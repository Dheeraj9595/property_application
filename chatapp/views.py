import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from groq import Groq

# Initialize Groq client
client = Groq(api_key="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")


# Define the system prompt


from rag.vector_store import retrieve_documents

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        retrived_docs = retrieve_documents(user_message)
        context = " ".join(retrived_docs) if retrived_docs else ""

        PROMPT = (f"Context: {context}\nYou are a assistant.\nAnswer questions related to docs which are in db or anything asked for.")

        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": PROMPT},  # System prompt
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
