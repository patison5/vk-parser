import vk

def get_members(groupid):  # Функция формирования базы участников сообщества в виде списка
    first = vk_api.groups.getMembers(group_id=groupid, v=5.92)  # Первое выполнение метода
    data = first["items"]  # Присваиваем переменной первую тысячу id'шников
    count = first["count"] // 1000  # Присваиваем переменной количество тысяч участников
    # С каждым проходом цикла смещение offset увеличивается на тысячу
    # и еще тысяча id'шников добавляется к нашему списку.
    for i in range(1, count + 1):
        data = data + vk_api.groups.getMembers(group_id=groupid, v=5.92, offset=i * 1000)["items"]
    return data


def save_data(data, filename="data.txt"):  # Функция сохранения базы в txt файле
    with open(filename, "w") as file:  # Открываем файл на запись
        # Записываем каждый id'шник в новой строке,
        # добавляя в начало "vk.com/id", а в конец перенос строки.
        for item in data:
            file.write("vk.com/id" + str(item) + "\n")


def enter_data(filename="data.txt"):  # Функция ввода базы из txt файла
    with open(filename) as file:  # Открываем файл на чтение
        b = []
        # Записываем каждую строчку файла в список,
        # убирая "vk.com/id" и "\n" с помощью среза.
        for line in file:
            b.append(line[9:len(line) - 1])
    return b


# Функция нахождения пересечений двух баз
def get_intersection(group1, group2):
    group1 = set(group1)
    group2 = set(group2)
    intersection = group1.intersection(group2)  # Находим пересечение двух множеств
    all_members = len(group1) + len(group2) - len(intersection)
    result = len(intersection) / all_members * 100  # Высчитываем пересечение в процентах
    #print("Пересечение аудиторий: ", round(result, 2), "%", sep="")
    print("Схожесть данных с предложенной группой: ", round(100 * len(intersection) / len(group2), 2), "%", sep="")
    return list(intersection)


# Функция объединения двух баз без повторов
def union_members(group1, group2):
    group1 = set(group1)
    group2 = set(group2)
    union = group1.union(group2)
    return list(union)


def remove_members(group1, group2):
    group2 = set(group2)
    group1 = set(group1)
    for item in group2:
        # group1 = group1.discard(item)
        group1.remove(group2, item)


    return list(group2)

if __name__ == "__main__":
    token = "0152bbbc0152bbbc0152bbbc04013f4323001520152bbbc5c995c1692c36bf31fb38a5d"
    session = vk.Session(access_token=token)
    vk_api = vk.API(session)

    goups_list = ["rust_iron",              "madfun",           "rustultimate",]
                  # "grandrust_server",       "rustfury",         "magicowrust",
                  # "chistobzden",            "travelerust",      "bloodrust",
                  # "dimonrust",              "rust_planet",      "dante_rust",
                  # "rustchance",             "magicrustfree",    "qqrust"]

    group_list_to_remove = ["redfederust"]

    result = get_members(goups_list[0])


    #Собираем большой список
    i = 1;
    while i < len(goups_list):
        gr = get_members(goups_list[i])         # берем участнико группы

        #print(f"[{goups_list[0:i:1]}] ({len(result)}) -> {goups_list[i]} ({len(gr)})")
        get_intersection(result, gr)            # получаем статистика его списка и ноой группы

        result = union_members(gr, result)      # Соединяем с сущестющим списком

        i += 1

    print(f"Всего: {len(result)} пользотелей")

    # Удаляем пользотелей из ггруп для ремуа
    i = 0;
    while i < len(group_list_to_remove):
        gr = get_members(group_list_to_remove[i])  # берем участнико группы

        print(f"[result] ({len(result)}) -> {group_list_to_remove[i]} ({len(gr)})")
        remove_members(result, gr)  # получаем статистика его списка и ноой группы

        i += 1


    print(f"Всего: {len(result)} уникальных пользотелей")
    save_data(result)