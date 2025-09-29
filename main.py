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

def getDiscipline(course_num):
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT name, day, pair_num FROM disciplines WHERE course_num = %s ORDER BY day, pair_num", (course_num,))
    
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

def getStudents(course_num):
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT name FROM students WHERE course_num = %s ORDER BY name", (course_num,))
    
    students = cur.fetchall()
    
    if students:
        print(Fore.GREEN + f"Студенты {course_num} курса:")
        for student in students:
            print(f"  - {student[0]}")
    else:
        print(Fore.YELLOW + f"На курсе {course_num} студентов не найдено")
    
    cur.close()
    conn.close()

def getDisciplines():
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM disciplines")
    
    disciplines = cur.fetchall()
    
    print(Fore.GREEN + "Все дисциплины:")
    print(Fore.CYAN + "ID | Название дисциплины | День недели | Номер пары | Номер курса")
    for disc in disciplines:
        # Преобразуем все элементы в строки и выводим через разделитель
        print(" | ".join(str(item) for item in disc))
    
    cur.close()
    conn.close()

def menu():
    for x in range(3):
        print('\n')
    print(Fore.GREEN + "   Выберите команду")
    print("1.Найти студента по id.")
    print("2.Все занятия по номеру курса.")
    print("3.Список всех студентов по номеру курса.")
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
            try:
                num = int(input("Введите номер курса: "))
                getStudents(num)
            except ValueError:
                print(Fore.RED + "Некоректнный ввод.")

            pressEnter()

        elif com == 4:
            getDisciplines()

            pressEnter()

        elif com == 5:

            
            pressEnter()

def pressEnter():
    input(Fore.CYAN + "Press enter...")

def main():
    interface()

main()