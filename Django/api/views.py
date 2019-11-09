from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, \
    HttpResponseServerError, JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import ObjectDoesNotExist

from problems.models import Problem, Tag
from problems.views import address_to_ll, ll_to_address
from users.models import Profile, User


def check_auth(token):
    return Profile.objects.get(user=1)  # FIXME: ОЧЕНЬ КОСТЫЛЬ
    try:
        token_type, token = token.split(':')
        if token_type == 'tg':
            return Profile.objects.get(tg_token=token)
        elif token_type == 'vk':
            return Profile.objects.get(vk_token=token)
        elif token_type == 'alice':
            return Profile.objects.get(alice_token=token)
        else:
            raise ValueError
    except ObjectDoesNotExist:
        return HttpResponseForbidden('Доступ запрещен')
    except (ValueError, AttributeError):
        return HttpResponseBadRequest('Отсутствует токен')


@csrf_exempt
@require_POST
def problem_new(request):
    profile = check_auth(request.POST.get('token'))
    if not isinstance(profile, Profile):
        return profile

    try:
        title = request.POST['title']
        description = request.POST['description']
        photo = request.POST.get('photo')
        tag = Tag.objects.get(name=request.POST['tag'])
    except KeyError as e:
        return HttpResponseBadRequest('Не все поля заполнены: ' + str(e.args[0]))

    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    address = request.POST.get('address')

    try:
        if latitude and longitude:
            latitude, longitude, address = ll_to_address(latitude, longitude)
        elif address:
            latitude, longitude, address = address_to_ll(address)
        else:
            return HttpResponseBadRequest('Отсутствует местоположение (координаты или адрес)')
    except Exception:
        return HttpResponseServerError('Ошибка Yandex API')

    try:
        problem = Problem(user=profile, title=title, description=description, photo=photo, tag=tag, latitude=latitude,
                          longitude=longitude, address=address)
        problem.save()
    except Exception:
        return HttpResponseServerError('Ошибка сохранения в БД')
    return HttpResponse()


@require_GET
def problems_list(request):
    objects = Problem.objects.all()

    problems = {'problems': [obj.json() for obj in objects]}
    response = JsonResponse(problems)
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_GET
def vote(request):
    try:
        id = int(request.GET['id'])
        change = int(request.GET['like'])
    except KeyError:
        return HttpResponseBadRequest()

    try:
        problem = Problem.objects.get(pk=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    else:
        problem.rating += change
        problem.save()
    return HttpResponse()
