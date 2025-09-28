from colorama import Fore, init
import psycopg2
from dataclasses import dataclass

init(autoreset=True)

@dataclass
class db_cfg:
    dbname: str = 'study'
    user: str = 'postgres'
    password: str = 'postgres'
    host: str = 'localhost'
    port: int = 5432

def getConn():
    cfg = db_cfg()
    conn = psycopg2.connect(dbname=cfg.dbname, user=cfg.user,
                            password=cfg.password, host=cfg.host,
                            port=cfg.port)
    
    return conn

def getStudent(id):
    conn = getConn()

    if conn is None:
        print(Fore.RED + "Ошибка подключения")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM student WHERE id = %s", (id, ))
    student = cur.fetchone()

    if student:
        print(Fore.GREEN + f"Найден студент: {student}")
    else:
        print(Fore.YELLOW + "Студент с таким ID не найден")

    cur.close()
    conn.close()

def getDiscipline(course_number):
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT name, day, pair_num FROM disciplines WHERE course_num = %s ORDER BY day, pair_num", (course_number,))
    
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    
    for day in days:
        cur.scroll(0, mode='absolute')
        
        day_disciplines = [(pair_num, name) for name, d, pair_num in cur.fetchall() if d == day]
        
        print(Fore.GREEN + f"\n{day.capitalize()}:" if day_disciplines else Fore.YELLOW + f"\n{day.capitalize()}:")
        
        for pair_num, name in day_disciplines:
            print(f"  {pair_num}. {name}")
        
        if not day_disciplines:
            print("  занятий нет")

    cur.close()
    conn.close()

def menu():
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

def interface():
    while True:
        com = menu()
        
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

def main():
    interface()

main()