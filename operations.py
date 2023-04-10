import json
from User import User


def recording(ids, name):
	with open('counting.txt', 'r') as f:
		count_msg = json.load(f)

	ids = str(ids)

	if ids not in count_msg.keys():
		user = User(ids, name)
		user = convert_to_data(user)
		count_msg[ids] = user
	else:
		user = convert_to_class(ids, count_msg[ids])
		if name != user.name:
			user.name = name
		user = convert_to_data(user)
		count_msg[ids] = user

	with open('counting.txt', 'w') as f:
		json.dump(count_msg, f)


def counting(id):
	with open('counting.txt', 'r') as f:
		count_msg = json.load(f)

	id = str(id)
	user = convert_to_class(id, count_msg[id])
	user.add_point(1)
	user = convert_to_data(user)

	count_msg[id] = user

	with open('counting.txt', 'w') as f:
		json.dump(count_msg, f)


def check(id):
	with open('counting.txt', 'r') as f:
		count_msg = json.load(f)

	id = str(id)
	user = count_msg[id]
	user = convert_to_class(id, user)

	if user.point >= int(75 + 0.4 * user.level * 100):
		user.add_level(1)
		user.point = 0

		new_user = convert_to_data(user)
		count_msg[id] = new_user

		with open('counting.txt', 'w') as f:
			json.dump(count_msg, f)

		return user.level

	return -1


def del_acc(ids):
	#удаление учатсника из карточки учатсника (counting.txt)

	with open('counting.txt', 'r') as f:
		count_msg = json.load(f)

	ids = str(ids)
	count_msg.pop(ids)

	with open('counting.txt', 'w') as f:
		json.dump(count_msg, f)


def add_point(id, points):
	with open('counting.txt', 'r') as f:
		count_msg = json.load(f)

	id = str(id)
	user = convert_to_class(id, count_msg[id])

	if type(points) == int:
		user.add_point(points)
	else:
		if 'нет' in user.title:
			user.title.remove('нет')
		user.title.append(points)

	user = convert_to_data(user)
	count_msg[id] = user

	with open('counting.txt', 'w') as f:
		json.dump(count_msg, f)


def del_point(name, points):
	with open('counting.txt', 'r') as f:
		count_msg = json.load(f)

	if type(points) == int:
		if points > count_msg[name][0]:
			count_msg[name][0] = 0
		else:
			count_msg[name][0] -= points
	else:
		if points in count_msg[name][2]:
			count_msg[name][2].remove(points)

	with open('counting.txt', 'w') as f:
		json.dump(count_msg, f)


def add_lvl(name, points):
	with open('counting.txt', 'r') as f:
		count_msg = json.load(f)

	count_msg[name][1] += points

	with open('counting.txt', 'w') as f:
		json.dump(count_msg, f)


def del_lvl(name, points):
	with open('counting.txt', 'r') as f:
		count_msg = json.load(f)

	if points > count_msg[name][1]:
		count_msg[name][1] = 0
	else:
		count_msg[name][1] -= points

	with open('counting.txt', 'w') as f:
		json.dump(count_msg, f)


def del_waif(user, name):
	with open('counting.txt', 'r') as f:
		count_msg = json.load(f)

	user = str(user)
	name = str(name)
	user_1 = convert_to_class(user, count_msg[user])
	user_2 = convert_to_class(name, count_msg[name])
	user_1.add_waif('нет')
	user_2.add_waif('нет')

	user_1 = convert_to_data(user_1)
	user_2 = convert_to_data(user_2)

	count_msg[user] = user_1
	count_msg[name] = user_2

	with open('counting.txt', 'w') as f:
		json.dump(count_msg, f)


def waif(user, name):
	with open('counting.txt', 'r') as f:
		count_msg = json.load(f)

	user = str(user)
	name = str(name)

	user_1 = convert_to_class(user, count_msg[user])
	user_2 = convert_to_class(name, count_msg[name])

	user_1.add_waif(user_2.id)
	user_2.add_waif(user_1.id)

	user_1 = convert_to_data(user_1)
	user_2 = convert_to_data(user_2)

	count_msg[user] = user_1
	count_msg[name] = user_2

	with open('counting.txt', 'w') as f:
		json.dump(count_msg, f)


def mycard(id):
	with open('counting.txt', 'r') as f:
		count_msg = json.load(f)

	id = str(id)

	return count_msg[id]


def transfer(server, mention='', name='', name_key=False):
	with open('members.txt', 'r') as f:
		servers = json.load(f)

	if not name_key:
		if server not in servers.keys():
			servers[server] = {}
	else:
		if mention not in servers[server].keys():
			servers[server][mention] = name

	with open('members.txt', 'w') as f:
		json.dump(servers, f)


def convert(server, mention):
	with open('members.txt', 'r') as f:
		servers = json.load(f)

	return servers[server][mention]


def convert_to_data(user):
	data = [user.name, user.point, user.level, user.title, user.waif]
	return data


def convert_to_class(id, data):
	user = User(id, data[0], data[1], data[2], data[3], data[4])
	return user
