import os

from backend.config import storage
from database.db_models import User, Object


def get_access_level_to_file(o_name: str) -> int | None:
    with storage:
        if storage.object_exists(o_name=o_name):
            object_data: Object = storage.get_object(o_name=o_name)
        else:
            print(f"Объекта {o_name} не существует")
            return None
        o_secure_level = object_data.secure_mark
        return o_secure_level


def read_file(user: str, o_name: str) -> None:
    o_access_level = int(get_access_level_to_file(o_name=o_name))
    with storage:
        u_access_level = int(storage.get_user(u_name=user).access_mark)
        if u_access_level <= o_access_level:
            object_data: Object = storage.get_object(o_name=o_name)
            file_uri = object_data.uri
            with open(file_uri, 'r') as f:
                data = f.read()
                print(f"Успешное чтение файла {o_name}")
                print(data)
        else:
            print("У вас нет прав на чтение этого файла")


def write_to_file(user: str, o_name: str, data: str) -> None:
    o_access_level = int(get_access_level_to_file(o_name=o_name))
    with storage:
        u_access_level = int(storage.get_user(u_name=user).access_mark)
        if u_access_level >= o_access_level:
            object_data = storage.get_object(o_name=o_name)
            file_uri = object_data.uri
            # print(file_uri)
            with open(file_uri, "a") as f:
                f.write(data)
            print(f"Файл {o_name} успешно изменен")
        else:
            print("У вас нет прав на чтение этого файла")


def create_object(user: str, o_name: str) -> None:
    open(f"./objects/{o_name}.txt", "x")
    filepath = os.path.abspath(o_name + ".txt")
    with storage:
        u_data: User = storage.get_user(u_name=user)
        # print(user_id[0])
        storage.create_object(o_name=o_name, o_user_id=u_data.id, o_secure_mark=u_data.access_mark, o_file_uri=filepath)
        print(f"Успешное создание объекта {o_name} по пути <{filepath}>")


def delete_object(user: str, o_name: str) -> None:
    filepath = os.path.abspath("./objects/" + o_name + ".txt")
    # print(filepath)
    with storage:
        os.remove(filepath)
        storage.delete_object(o_name=o_name)
        print(f"Успешно удален объект {o_name}")


def get_files() -> None:
    with storage:
        objects_list: list[Object] = storage.get_all_objects()
        print("Ваши права на объекты в системе:")
        for cur_object in objects_list:
            access_level = get_access_level_to_file(o_name=cur_object.name)
            print(f"\t {cur_object.name} : access_level={access_level}")
