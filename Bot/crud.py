from aiohttp import ClientSession
import json


async def get_pieces(sort_by: str = None, genre: str = None, name: str = None):
    data = {'sort_by': sort_by, 'genre': genre, 'name': name}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/pieces/', data=json_data) as response:

            response = await response.json()
            if not name:
                return [dict_piece['name'] for dict_piece in response]
            else:
                return response[0]['description']
