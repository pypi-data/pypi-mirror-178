from classes import class_slots, class_no_slots
from lists import list_func1, list_func2, list_func3, list_func4, list_func5
from base import start

def test_all():
	start('classes', ['classes.classes_slots'], globals())
	start('lists', ['lists.lists'], globals())

if __name__ == '__main__':
	test_all()

