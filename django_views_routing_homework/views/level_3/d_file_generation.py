"""
В этом задании вам нужно научиться генерировать текст заданной длинны и возвращать его в ответе в виде файла.

- ручка должна получать длину генерируемого текста из get-параметра length;
- дальше вы должны сгенерировать случайный текст заданной длины. Это можно сделать и руками
  и с помощью сторонних библиотек, например, faker или lorem;
- дальше вы должны вернуть этот текст, но не в ответе, а в виде файла;
- если параметр length не указан или слишком большой, верните пустой ответ со статусом 403

Вот пример ручки, которая возвращает csv-файл: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
С текстовым всё похоже.

Для проверки используйте браузер: когда ручка правильно работает, при попытке зайти на неё, браузер должен
скачивать сгенерированный файл.
"""

from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed, HttpResponseForbidden
from lorem import paragraph
MAX_TEXT_LENGTH = 5000


def generate_random_text(text_length):
    generated_text = paragraph()
    while len(generated_text) < text_length:
        generated_text += '\n' + paragraph()
    return generated_text[:text_length]


def generate_file_with_text_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        text_length = int(request.GET.get('length', None))
        if text_length and text_length < MAX_TEXT_LENGTH:
            random_text = generate_random_text(text_length)
            response = HttpResponse(
                content_type="text/plain",
                headers={"Content-Disposition": 'attachment; filename="attachment.txt"'},
            )
            response.writelines(random_text)
            return response
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET'])
