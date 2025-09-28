from colorama import Fore
from def_api import *

def interface():

    while True:
        com = _menu()
        
        if com == 6:
            return

        elif com == 1:
            try:
                id = int(input("Введите id студента: "))
                getStudent(id)
            except ValueError:
                print(Fore.RED + "ID некоректнный.")
            
            pressEnter()

        elif com == 2:
            try:
                num = int(input("Введите номер курса: "))
                getDiscipline(num)
            except ValueError:
                print(Fore.RED + "Некоректнный ввод.")
            
            pressEnter()

        elif com == 3:
            print("Выбрана опция 3")
            # Код для опции 3

        elif com == 4:
            print("Выбрана опция 4")
            # Код для опции 4

        elif com == 5:
            print("Выбрана опция 5")
            # Код для опции 5

def pressEnter():
    input(Fore.CYAN + "Press enter...")

def _menu():
    for x in range(3):
        print('\n')
    print(Fore.GREEN + "   Выберите команду")
    print("1.Найти студента по id.")
    print("2.Все занятия по номеру курса.")
    print("3.Список всех студентов.")
    print("4.Полное рассписание дисциплин.")
    print("5.Добавить нового студента.")
    print("6.Выйти.")

    try:
        command = int(input("\nВведите команду: "))
    except ValueError:
        print(Fore.RED + "Некоректнный ввод.")
        return 0

    return command