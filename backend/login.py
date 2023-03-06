"""
    PATCH 8.00

    Heroes:
        -Broodmother deleted from the game
        -Lina:
            -Attack range decreased to 150
            -Fiery Soul now have 3 stacks rather the 7 in previous patch
        -Pudge:
            -Now can be peaked by both sides even he was peaked by one of the teams
            -Now pudge can't de banned
        -Muerta:
            -Added in the game
        -Axe:
            -Now Axe have implemented Blink Dagger, it can't be toggled down by getting hit
"""
from backend.config import storage


def login():
    name = input('Введите имя пользователя: \n')
    flag = False
    while not flag:
        with storage:
            flag = storage.user_exists(u_name=name)
        if not flag:
            print(f"Не удалось войти под указанным пользователем {name}")
            continue
        else:
            print(f"Вы успешно вошли под пользователем {name}")
            break
    # тут что делать когда вошли в систему
