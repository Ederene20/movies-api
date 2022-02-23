from django.http import JsonResponse


def ping(request):
    data = {
        "ping": "pong!"
    }
    return JsonResponse(data)


def hello(request):
    data = {
        'greetings': 'hello!'
    }
    return JsonResponse(data)