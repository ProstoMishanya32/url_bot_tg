import json

async def add_admin(user_id, nickname):
    with open('modules/json_files/admins.json', 'r', encoding='utf-8') as f:
        admins = json.load(f)
        id_users = []
        for i in admins:
            id_users.append(i['user_id'])
    if user_id not in id_users:
        admins.append({"user_id":user_id, "nickname":nickname})
    with open('modules/json_files/admins.json', 'w', encoding='utf-8') as f:
        json.dump(admins, f, ensure_ascii=False)


async def remove_admin(user_id):
    with open('modules/json_files/admins.json', 'r', encoding='utf-8') as f:
        admins = json.load(f)
    try:
        remove = []
        for i in admins:
            if int(user_id) == i['user_id']:
                id_user = i['user_id']
                nickname = i['nickname']
                admin = True
            else:
                admin = False
        admins.remove({"user_id":id_user, "nickname":nickname})
    except Exception as i:
        admin = False
    with open('modules/json_files/admins.json', 'w', encoding='utf-8') as f:
        json.dump(admins, f, ensure_ascii=False)
    return admin


async def see_admins():
    with open('modules/json_files/admins.json', 'r', encoding='utf-8') as f:
        list_admins = []
        admins = json.load(f)
        current_position = 1
        for i in admins:
            character = dict()
            character['user_id'] = i['user_id']
            character['nickname'] = i['nickname']
            character['position'] = current_position
            list_admins.append(character)
            current_position += 1
        return list_admins

async def get_admins():
    with open('modules/json_files/admins.json', 'r', encoding='utf-8') as f:
        admins = json.load(f)
        id_users = []
        for i in admins:
            id_users.append(i['user_id'])
    return id_users