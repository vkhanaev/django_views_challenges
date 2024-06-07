"""
В этом задании вам нужно реализовать вьюху, которая валидирует данные о пользователе.

- получите json из тела запроса
- проверьте, что данные удовлетворяют нужным требованиям
- если удовлетворяют, то верните ответ со статусом 200 и телом `{"is_valid": true}`
- если нет, то верните ответ со статусом 200 и телом `{"is_valid": false}`
- если в теле запроса невалидный json, вернуть bad request

Условия, которым должны удовлетворять данные:
- есть поле full_name, в нём хранится строка от 5 до 256 символов
- есть поле email, в нём хранится строка, похожая на емейл
- есть поле registered_from, в нём одно из двух значений: website или mobile_app
- поле age необязательное: может быть, а может не быть. Если есть, то в нём хранится целое число
- других полей нет

Для тестирования рекомендую использовать Postman.
Когда будете писать код, не забывайте о читаемости, поддерживаемости и модульности.
"""
import json
import re
from typing import Dict

from django.core.exceptions import BadRequest
from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed, JsonResponse


def data_is_valid(data: Dict[str, str | int | None]) -> bool:
    if 'full_name' not in data or not (5 <= len(data['full_name']) <= 256):
        return False

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if 'email' not in data or not re.match(email_regex, data['email']):
        return False

    if 'registered_from' not in data or data['registered_from'] not in {'website', 'mobile_app'}:
        return False

    if 'age' in data and not isinstance(data['age'], int):
        return False

    allowed_fields = {'full_name', 'email', 'registered_from', 'age'}
    if any(field not in allowed_fields for field in data):
        return False

    return True


def validate_user_data_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data_is_valid(data):
                return JsonResponse({"is_valid": True}, status=200)
            return JsonResponse({"is_valid": False}, status=200)
        except Exception as e:
            raise BadRequest('Invalid request.')
    return HttpResponseNotAllowed(permitted_methods=['POST'])
