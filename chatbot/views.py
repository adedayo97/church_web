import json
import openai
from django.http import JsonResponse
from .models import ChatMessage
from django.views.decorators.csrf import csrf_exempt
import logging
from random import choice

logger = logging.getLogger(__name__)

# Hardcoded API key (as requested)
OPENAI_API_KEY = "***REMOVED***"

# Predefined responses for when OpenAI API is unavailable
PREDEFINED_RESPONSES = [
    "Peace be with you! Our spiritual guidance system is currently at capacity. Please try again later or contact us directly.",
    "Thank you for your message. We're experiencing high volumes of prayer requests right now. Your question is important to us.",
    "Bless you for reaching out. Our virtual assistant is currently in meditation. Please try again shortly.",
    "We appreciate your patience. Our digital deacons are currently occupied with other spiritual matters.",
    "Your message has been received and will be lifted up in prayer. Please check back later for a response."
]

FAQ_RESPONSES = {
    "service times": "Our regular services are Sunday at 9am and 11am, with Wednesday prayer meeting at 7pm.",
    "location": "We're located at 123 Faith Avenue, Spiritual City. All are welcome!",
    "children": "We have wonderful Sunday School programs for all ages during both services.",
    "involved": "There are many ways to serve! Please visit our ministries page or talk to any pastor.",
    "counseling": "Yes, we offer pastoral counseling. Please contact the church office to schedule an appointment.",
    "beliefs": "We believe in the Holy Trinity and follow the teachings of Jesus Christ as revealed in Scripture."
}

@csrf_exempt
def chat_response(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            try:
                data = json.loads(request.body)
                user_message = data.get('message', '').strip().lower()
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)

            if not user_message:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)

            # First check if this is a FAQ question
            for keyword, response in FAQ_RESPONSES.items():
                if keyword in user_message:
                    bot_response = response
                    break
            else:
                # If not a FAQ, try OpenAI (with fallback)
                try:
                    client = openai.OpenAI(api_key=OPENAI_API_KEY)
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "system", 
                                "content": "You are a helpful church assistant. Provide warm, spiritual responses to questions about church services, events, and Christian teachings."
                            },
                            {
                                "role": "user", 
                                "content": user_message
                            }
                        ],
                        temperature=0.7,
                        max_tokens=150
                    )
                    bot_response = completion.choices[0].message.content
                except openai.OpenAIError as e:
                    logger.warning(f"OpenAI API Error - using fallback response: {str(e)}")
                    bot_response = choice(PREDEFINED_RESPONSES)
                except Exception as e:
                    logger.error(f"Unexpected OpenAI error: {str(e)}")
                    bot_response = "God's grace is sufficient, even when technology fails us. Please try again later."

            # Save to database
            ChatMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                message=user_message,
                response=bot_response
            )

            return JsonResponse({'response': bot_response})

        except Exception as e:
            logger.error(f"Unexpected server error: {str(e)}")
            return JsonResponse({
                'response': "An unexpected error occurred in our prayer chain. Please try again."
            }, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)