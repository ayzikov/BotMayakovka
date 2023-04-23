import json

from .serializers import PieceSerializerName, PieceSerializerDesc
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Piece

def get_dict_from_json(val, request):
    json_data = request.body.decode('utf-8')  # преобразование байтовой строки в строку
    data = json.loads(json_data)  # преобразование JSON-строки в словарь Python
    return data.get(val)  # получение значения по ключу 'val'


class PieceView(APIView):
    def get(self, request: Request):
        """
                Обрабатывает GET-запрос к API-эндпоинту.

                Поддерживаемые GET-параметры:
                - sort_by: параметр сортировки (name, date, genre);
                - genre: жанр произведения (используется только при sort_by=genre);
                - id: id произведения (используется только при отсутствии sort_by).

                Если sort_by не указан, то возвращает объект Piece, чье имя начинается с указанного в GET-параметре name.

                :param request: объект Request, содержащий информацию о запросе;
                :return: объект Response с сериализованными данными.
                """
        random = get_dict_from_json(val='random', request=request)
        id = get_dict_from_json(val='id', request=request)
        sort_by = get_dict_from_json(val='sort_by', request=request)
        description = get_dict_from_json(val='description', request=request)
        image = get_dict_from_json(val='image', request=request)

        if sort_by:
            if sort_by == 'name':
                res = Piece.objects.all().order_by('name').values('name', 'id')
            if sort_by == 'date':
                res = Piece.objects.all().order_by('date').values('name', 'id')
            if sort_by == 'genre':
                genre = get_dict_from_json(val='genre', request=request)
                res = Piece.objects.filter(genre=genre).values('name', 'id')
            if sort_by == 'non_popular':
                res = Piece.objects.filter(little_known=True).values('name', 'id')

            return Response(PieceSerializerName(res, many=True).data)

        elif random:
            res = Piece.objects.order_by('?').first()
            return Response(PieceSerializerName(res).data)

        elif image:
            res = Piece.objects.get(id=id)
            image_path = res.image.path  # Получаем путь к файлу изображения
            return Response(image_path)

        elif id and not description:
            res = Piece.objects.filter(id=id).values('name', 'id')
            return Response(PieceSerializerName(res, many=True).data)

        elif description:
            res = Piece.objects.filter(id=id).values('name',
                                                     'id',
                                                     'description_piece',
                                                     'description_piece_detailed',
                                                     'description_play')

            return Response(PieceSerializerDesc(res, many=True).data)






