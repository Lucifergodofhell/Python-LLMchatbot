from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests
from langchain_ollama import OllamaLLM

# GET view: Serves the chatbot HTML page
def chatbot_page(request):
    return render(request, 'chatbot.html', {})  # templates/chatbot.html use kar

# POST view: Handles AI response via Ollama
@csrf_exempt
@require_http_methods(["POST"])
def AIresponce(request):  # Fixed: request as first arg
    print(request.body)  # Debug print
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()  # Extract message from JSON
        
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)
        
        print(f"User message: {user_message}")  # Debug print
        
        # Ollama integration
        ollama_url = 'http://127.0.0.1:11434/'
        llm = OllamaLLM(model='llama3.2:3b', base_url=ollama_url);
        
        response = llm.invoke([{"role": "user", "content": user_message}])
        print(f"Ollama response: {response}")  # Debug print
        return JsonResponse({'response': response});
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Connection error: {str(e)}'}, status=500)
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)