import json
from django.http import HttpResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from .models import Thing


@csrf_exempt
def things_api(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        thing = Thing.objects.create(**data)
        return HttpResponse(serialize('json', [thing]),
                            content_type='application/json')
    return HttpResponse('', status_code=400, content_type='application/json')


@csrf_exempt
def thing_api(request, pk):
    if request.method not in ('POST', 'GET'):
        return HttpResponse(
            '', status_code=400, content_type='application/json')

    thing = Thing.objects.get(pk=pk)

    if request.method == 'POST':
        # This is senseless, but simulates three read operations to the replica
        thing = Thing.objects.get(pk=pk)
        thing = Thing.objects.get(pk=pk)

        data = json.loads(request.body.decode('utf-8'))
        thing.color = data['color']
        thing.save()

        # This is senseless, but simulates a read operation to the primary
        thing = Thing.objects.get(pk=pk)

    return HttpResponse(serialize('json', [thing]),
                        content_type='application/json')
