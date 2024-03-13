from django.shortcuts import render
import openai, os
from decouple import config
from openai import ChatCompletion
from django.http import JsonResponse
from pptx import Presentation



api_key = config('OPENAI_KEY')

def chatbot(request):
    chatbot_response = None
    if request.method == 'POST':
        if api_key is not None:
            openai.api_key = api_key
            user_input = request.POST.get('user_input')
            prompt = user_input
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=256,
                temperature=0.5
            )
            print(chatbot_response)
            chatbot_response = response.choices[0]["text"]

    return render(request, 'users/chatbot.html', {'chatbot_response': chatbot_response})




def generate_ppt(request):
    if request.method == 'POST':
        prompts = request.POST.get('prompt')
        # Generate PowerPoint slides based on the prompt
        prs = Presentation()
        for prompt in prompts:
            slide = prs.slides.add_slide(prs.slide_layouts[0])
            slide.shapes.title.text = prompt
        
        # Save the presentation file
        file_path = 'presentation.pptx'
        prs.save(file_path)
        # Return JSON response with file URL
        return JsonResponse({'file_url': file_path})
    return render(request, 'users/generate.html')