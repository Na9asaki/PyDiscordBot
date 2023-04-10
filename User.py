class User:
    def __init__(self, id, name='', point=0, level=0, title=None, waif='нет'):
        if title is None:
            title = ['нет']
        self.name = name
        self.point = point
        self.level = level
        self.title = title
        self.waif = waif
        self.id = id

    def rename(self, new_name):
        self.name = new_name

    def add_point(self, amount):
        self.point += amount

    def add_level(self, amount):
        self.level += amount

    def add_title(self, new_title):
        self.title.append(new_title)

    def add_waif(self, name_waif):
        self.waif = name_waif
