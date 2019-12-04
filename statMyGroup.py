'''
Данный модуль служит для отслеживания активности в собственной группе.
Программа получает список всех подписчиков, анализирует каждого на предмет нахождения его в онлайне и сохраняет статистику.
'''
import datetime
import time
import vk
import json
from prettytable import PrettyTable

tableToShow = PrettyTable()

def get_members(groupid):
    first = vk_api.groups.getMembers(group_id=groupid, v=5.92)
    data  = first["items"]
    count = first["count"] // 1000

    for i in range(1, count + 1):
        data = data + vk_api.groups.getMembers(group_id=groupid, v=5.92, offset=i*1000)["items"]
    return data


def save_data(data, filename="onlineMonitoringData.txt"):  # Функция сохранения базы в txt файле
    with open(filename, "a+") as file:  # Открываем файл на запись
        # Записываем каждый id'шник в новой строке,
        # добавляя в начало "vk.com/id", а в конец перенос строки.
        file.write(str(data) + "\n")

def start ():
    groupUsersIDs = get_members("redfederust")
    tableToShow.field_names = ["ID", "First Name", "Last Name", "Status"]
    ID = 0
    onlineList = []

    onlineList.append({"Data": [], "time": str(datetime.datetime.now())})

    for userID in groupUsersIDs:
        test = vk_api.users.get(user_id=userID, fields='online, last_seen', v=5.92)
        #print (test)
        ID += 1

        if test[0]['online']:
            tableToShow.add_row([ID, test[0]['first_name'], test[0]['last_name'], "online"])
            #print (f"{test[0]['first_name']} {test[0]['last_name']} is online now")
            onlineList[0]['Data'].append({"first_name": test[0]['first_name'], "last_name":  test[0]['last_name']})
        else:
            tableToShow.add_row([ID, test[0]['first_name'], test[0]['last_name'], "offline"])
            #print(f"{test[0]['first_name']} {test[0]['last_name']} is offline now")


    print(tableToShow)

    if (len(onlineList[0]["Data"]) % 10 == 2) or (len(onlineList[0]["Data"]) % 10 == 3) or (len(onlineList[0]["Data"]) % 10 == 4):
        print(f"В онлайне сейчас: {len(onlineList[0]['Data'])} человека")
    else:
        print(f"В онлайне сейчас: {len(onlineList[0]['Data'])} человек")

    print(onlineList[0]["Data"])
    save_data(onlineList)

if __name__ == "__main__":
    token = "0152bbbc0152bbbc0152bbbc04013f4323001520152bbbc5c995c1692c36bf31fb38a5d"
    session = vk.Session(access_token=token)
    vk_api = vk.API(session)


    while True:
        start()

        currentTime = datetime.datetime.now()
        print(f"Last update was at {currentTime}")
        time.sleep(15)  # in seconds