import json

from .serializers import PieceSerializerName, PieceSerializerDesc
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Piece

def get_dict_from_json(val, request):
    json_data = request.body.decode('utf-8')  # преобразование байтовой строки в строку
    data = json.loads(json_data)  # преобразование JSON-строки в словарь Python
    return data.get(val)  # получение значения по ключу 'name'


class PieceView(APIView):
    def get(self, request: Request):
        """
                Обрабатывает GET-запрос к API-эндпоинту.

                Поддерживаемые GET-параметры:
                - sort_by: параметр сортировки (name, date, genre);
                - genre: жанр произведения (используется только при sort_by=genre);
                - name: имя произведения (используется только при отсутствии sort_by).

                Если sort_by не указан, то возвращает объект Piece, чье имя начинается с указанного в GET-параметре name.

                :param request: объект Request, содержащий информацию о запросе;
                :return: объект Response с сериализованными данными.
                """

        sort_by = get_dict_from_json(val='sort_by', request=request)

        if sort_by:
            if sort_by == 'name':
                res = Piece.objects.all().order_by('name').values('name')
            if sort_by == 'date':
                res = Piece.objects.all().order_by('date').values('name')
            if sort_by == 'genre':
                genre = get_dict_from_json(val='genre', request=request)
                res = Piece.objects.filter(genre=genre).values('name')

            return Response(PieceSerializerName(res, many=True).data)

        else:
            name = get_dict_from_json(val='name', request=request)
            res = Piece.objects.filter(name__startswith=name).values('description')

            return Response(PieceSerializerDesc(res, many=True).data)

