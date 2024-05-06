from django.shortcuts import render
from django.http import JsonResponse
from .module1_live import SpeechRecognitionApp

def module1_view(request):
    if request.method == 'POST':
        # Handle AJAX request to start speech recognition
        app = SpeechRecognitionApp()
        transcription = app.start_listening()
        return JsonResponse({'transcription': transcription})
    else:
        return render(request, 'module1.html')


def module2_view(request):
    if request.method == 'POST' and request.FILES['text_file']:
        text_file = request.FILES['text_file']
        file_path = os.path.join(settings.MEDIA_ROOT, text_file.name)

        with open(file_path, 'wb') as destination:
            for chunk in text_file.chunks():
                destination.write(chunk)

        result = process_text_file(file_path)
        os.remove(file_path)
        return HttpResponse(result)
    else:
        return render(request, 'module2.html')
