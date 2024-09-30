import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import random

# Токен ВК бота
VK_TOKEN = 'vk1.a.Dc4z0Py3pdKK9ZM_8G3RpTEUrJa-6_4VEfjj_zuf3lEo_T3r5BAMZEcAYUB0-uORHYR-tYGS6Xj9fUjDI72sC9CwPfK0HmRiu3h6aEKe6HJF3bYnxYOah4r6Y_6qBIFBCz7Pa4DzHn0-_Ack9yi3zI41Xb6bk0Cb0eEtryiTRkL7agmhP4Xft2mjy9e4Bbp-yVFviDJbu-NRHZCzHHPAjg'

# Расширенный список рецептов
recipes = [
    {
        "name": "Борщ",
        "ingredients": "Свекла, картофель, морковь, капуста, томатная паста, чеснок, лук, уксус, лавровый лист, мясо.",
        "steps": "1. Нарезать овощи. 2. Обжарить свеклу с уксусом. 3. Сварить мясо и добавить овощи. 4. Подавать со сметаной."
    },
    {
        "name": "Плов",
        "ingredients": "Рис, мясо, лук, морковь, чеснок, зира, масло, соль.",
        "steps": "1. Обжарить мясо. 2. Добавить лук и морковь. 3. Добавить рис, залить водой и тушить до готовности."
    },
    {
        "name": "Мясо по-французски",
        "ingredients": "Свинина, картофель, сыр, лук, майонез, соль, перец.",
        "steps": "1. Нарезать свинину кусочками, отбить и выложить на противень. 2. Добавить лук и картофель, посыпать сыром. 3. Запекать при 180°C до готовности."
    },
    {
        "name": "Паста с курицей",
        "ingredients": "Паста, куриное филе, сливки, сыр, чеснок, соль, перец.",
        "steps": "1. Отварить пасту. 2. Обжарить курицу с чесноком. 3. Добавить сливки, сыр и тушить. 4. Смешать с пастой."
    },
    {
        "name": "Рис с овощами",
        "ingredients": "Рис, морковь, лук, болгарский перец, кукуруза, горошек, соль, масло.",
        "steps": "1. Отварить рис. 2. Обжарить овощи. 3. Смешать рис с овощами и тушить несколько минут."
    },
    {
        "name": "Лазанья",
        "ingredients": "Листы лазаньи, фарш, помидоры, сыр, соус бешамель, лук, чеснок, соль, перец.",
        "steps": "1. Обжарить фарш с луком и чесноком. 2. Добавить томаты. 3. Собрать лазанью слоями, чередуя с соусом и сыром. 4. Запекать при 180°C до золотистой корочки."
    },
    {
        "name": "Гречка с грибами",
        "ingredients": "Гречка, шампиньоны, лук, масло, соль, перец.",
        "steps": "1. Отварить гречку. 2. Обжарить грибы с луком. 3. Смешать грибы с гречкой, тушить несколько минут."
    },
    {
        "name": "Запеканка из картофеля",
        "ingredients": "Картофель, яйца, молоко, сыр, соль, перец.",
        "steps": "1. Нарезать картофель, выложить в форму. 2. Взбить яйца с молоком и залить картофель. 3. Посыпать сыром и запекать при 180°C до готовности."
    },
]


# Функция для создания клавиатуры с блюдами
def create_dish_keyboard():
    keyboard = {
        "one_time": False,
        "buttons": []
    }

    for recipe in recipes:
        keyboard["buttons"].append([{
            "action": {
                "type": "text",
                "label": recipe["name"]
            },
            "color": "primary"
        }])

    return json.dumps(keyboard)


# Функция для получения рецепта по названию
def get_recipe_by_name(name):
    for recipe in recipes:
        if recipe['name'].lower() == name.lower():
            return f"{recipe['name']}\nИнгредиенты: {recipe['ingredients']}\nПошаговый рецепт: {recipe['steps']}"
    return None


# Инициализация бота
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def send_message(user_id, message, keyboard=None):
    vk.messages.send(user_id=user_id, message=message, random_id=random.randint(1, 1000), keyboard=keyboard)


# Основной цикл прослушивания сообщений
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        request = event.text.lower()

        # Если пользователь запросил меню с блюдами
        if 'меню' in request:
            send_message(event.user_id, "Выберите блюдо:", create_dish_keyboard())
        else:
            # Проверяем, соответствует ли текст названию блюда
            recipe = get_recipe_by_name(request)
            if recipe:
                send_message(event.user_id, recipe)
            else:
                send_message(event.user_id, "Напиши 'меню', чтобы получить список блюд.")
