"""
В этом задании вам нужно реализовать ручку, которая принимает на вход ник пользователя на Github,
а возвращает полное имя этого пользователя.

- имя пользователя вы узнаёте из урла
- используя АПИ Гитхаба, получите информацию об этом пользователе (это можно сделать тут: https://api.github.com/users/USERNAME)
- из ответа Гитхаба извлеките имя и верните его в теле ответа: `{"name": "Ilya Lebedev"}`
- если пользователя на Гитхабе нет, верните ответ с пустым телом и статусом 404
- если пользователь на Гитхабе есть, но имя у него не указано, верните None вместо имени
"""
from typing import Any

import requests
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseNotFound


def get_user_info_from_github(github_username: str) -> tuple[int, Any]:
    github_url = 'https://api.github.com/users/%s' % github_username
    r = requests.get(github_url)
    return r.status_code, r.json()


def fetch_name_from_github_view(request: HttpRequest, github_username: str) -> HttpResponse:
    status, user_info = get_user_info_from_github(github_username)
    if status == 200:
        data = {"name": user_info['name']}
        return JsonResponse(status=status, data=data)
    else:
        return HttpResponse(status=status)
