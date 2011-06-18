from django.shortcuts import render_to_response


def terminator_index(request):
    return render_to_response('index.html')


