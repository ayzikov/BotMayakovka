import crud_pieces

all_pieces_text = 'Здесь ты можешь выбрать порядок знакомства с пьесами или предоставить право выбора его величеству рандому'
mood_pieces_text = 'Специфический юмор XIX века или трагедия, разрывающая душу, решать тебе'
alphabet_text = 'Так ты намного быстрее найдешь нужную пьесу'
date_text = 'Именно в таком порядке пьесы выходили из-под пера автора и можно проследить как менялось его отношение к жизни'
comedi_text = 'В конце все герои останутся живы, но жизнь их не сахар'
drama_text = 'Рекомендуем приготовить платочки, финал будет жестким'
info_piece_text = 'Информация о пьесе'
main_menu_text = 'Главное меню'
non_popular_text = 'Скорее всего, после прочтения можно будет блеснуть знаниями в кругу умных людей'
about_authors_text = f'На фото создатели этого прекрасного бота:\n\n' \
                     f'Сергеева Кира\n' \
                     f'Айзиков Никита\n' \
                     f'Герман Светлана'

text_sources = 'Источники информации:\n\n' \
               '· https://cyberleninka.ru/\n\n' \
               '· https://ru.wikipedia.org/wiki/\n\n' \
               '· http://ostrovskiy.lit-info.ru/\n\n' \
               '· https://www.sberbank.com/promo/kandinsky\n\n'


async def hello_text(name):
    return f'Привет {name}!\n' \
           f'Этот бот расскажет тебе о пьесе и подскажет, где посмотреть постановку'

async def text_user_stats(res: dict):
    return f'Статистика по количеству пользователй\n\n' \
           f'{res["all_users"]} - Пользователей за все время\n' \
           f'{res["day_users"]} - Пользователей за день\n' \
           f'{res["week_users"]} - Пользователей за неделю'


async def text_actions_stats(res: dict):
    return f'Статистика по количеству кликов\n\n' \
           f'{res["all_actions"]} - Кликов за все время\n' \
           f'{res["day_actions"]} - Кликов за день\n' \
           f'{res["week_actions"]} - Кликов за неделю'


async def text_comands_stats(res: dict):
    sort_res_tuples = sorted(res.items(), key=lambda el: el[1], reverse=True)
    res_list = "\n".join([f'{value} - {comand}' for comand, value in sort_res_tuples])
    return f'Статистика по командам\n\n' \
           f'{res_list}'
