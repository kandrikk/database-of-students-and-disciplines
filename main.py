from colorama import Fore, init
import psycopg2

init(autoreset=True)

def getConn():
    conn = psycopg2.connect(dbname='study', user='postgres',
                            password='postgres', host='localhost',
                            port=5432)
    
    return conn

def getStudent(id):
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id = %s", (id, ))
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
    
    day_week = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    
    for day in day_week:
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
    cur.execute("SELECT * FROM disciplines ORDER BY id")
    
    disciplines = cur.fetchall()
    
    headers = ["ID", "Название дисциплины", "День недели", "Номер пары", "Номер курса"]
    
    column_widths = [len(header) for header in headers]
    
    for disc in disciplines:
        for i, value in enumerate(disc):
            column_widths[i] = max(column_widths[i], len(str(value)))
    
    header_line = " | ".join(header.ljust(column_widths[i]) for i, header in enumerate(headers))
    print(Fore.GREEN + header_line)
    print("-" * len(header_line))
    
    for disc in disciplines:
        row = " | ".join(str(value).ljust(column_widths[i]) for i, value in enumerate(disc))
        print(row)
    
    cur.close()
    conn.close()

def putStudent(name, course_num):
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения")
        return
    
    cur = conn.cursor()
    
    try:
        cur.execute("INSERT INTO students (name, course_num) VALUES (%s, %s)", (name, course_num))
        conn.commit()
        print(Fore.GREEN + f"Студент {name} успешно добавлен на курс {course_num}")
    except psycopg2.Error as e:
        print(Fore.RED + f"Ошибка при добавлении студента: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def putDiscipline(name, day, pair_num, course_num):
    day_week = ["понедельник", "вторник", "среда", "четверг", "пятница"]

    if (day not in day_week) or (pair_num > 9) or (course_num > 8):
        print(Fore.RED + "Некоректнные данные")
        return

    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения")
        return
    
    cur = conn.cursor()
    
    try:
        cur.execute("INSERT INTO disciplines (name, day, pair_num, course_num) VALUES (%s, %s, %s, %s)"
                    , (name, day, pair_num, course_num))
        conn.commit()
        print(Fore.GREEN + f"Дисциплина {name} успешно добавлена на курс {course_num} в {day}, {pair_num} парой")
    except psycopg2.Error as e:
        print(Fore.RED + f"Ошибка при добавлении дисциплина: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def deleteStudent(id):
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения")
        return
    
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM students WHERE id = %s", (id, ))

        conn.commit()
        print(Fore.GREEN + f"Студент с ID = {id} удален.")
    except psycopg2.Error as e:
        print(Fore.RED + f"Ошибка при удаление студента: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def deleteDiscipline(id):
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения")
        return
    
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM disciplines WHERE id = %s", (id, ))

        conn.commit()
        print(Fore.GREEN + f"Занятия с ID = {id} удалено.")
    except psycopg2.Error as e:
        print(Fore.RED + f"Ошибка при удаление занятия: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def menu():
    for x in range(3):
        print('\n')
        
    print(Fore.GREEN + "   Выберите команду")
    print("a.Найти студента по ID.")
    print("b.Все занятия по номеру курса.")
    print("c.Список всех студентов по номеру курса.")
    print("d.Полное рассписание дисциплин.")
    print("e.Добавить нового студента.")
    print("f.Добавить занятия в расписание.")
    print("g.Удаление студента по ID.")
    print("h.Удаление занятия по ID.")
    print("i.Выйти.")

    varib = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    command = input("\nВведите команду: ")
    if command not in varib:
        print(Fore.RED + "Некоректный ввод.")
        pressEnter()
        return 0

    return command

def interface():
    while True:
        com = menu()

        if com == 'a':
            try:
                id = int(input("Введите id студента: "))
                getStudent(id)
            except ValueError:
                print(Fore.RED + "ID некоректнный.")
            
            pressEnter()

        elif com == 'b':
            try:
                num = int(input("Введите номер курса: "))
                getDiscipline(num)
            except ValueError:
                print(Fore.RED + "Некоректнный ввод.")
            
            pressEnter()

        elif com == 'c':
            try:
                num = int(input("Введите номер курса: "))
                getStudents(num)
            except ValueError:
                print(Fore.RED + "Некоректнный ввод.")

            pressEnter()

        elif com == 'd':
            getDisciplines()

            pressEnter()

        elif com == 'e':
            try:
                name = input("Введите имя студента: ")
                num_course = int(input("Введите номер курса: "))
                putStudent(name, num_course)
            except ValueError:
                print(Fore.RED + "Некоректнный ввод.")
            
            pressEnter()

        elif com == 'f':
            try:
                name = input("Введите название дисциплины: ")
                day = input("Введите день занятия: ").strip()
                pair_num = int(input("Введите номер пары: "))
                course_num = int(input("Введите номер курса: "))

                putDiscipline(name, day, pair_num, course_num)

            except ValueError:
                print(Fore.RED + "Некоректнный ввод")

            pressEnter()

        elif com == 'g':
            try:
                id = int(input("Введите ID: "))
                deleteStudent(id)
                
            except ValueError:
                print(Fore.RED + "Некоректнный ввод")

            pressEnter()

        elif com == 'h':
            try:
                id = int(input("Введите ID: "))
                deleteDiscipline(id)
                
            except ValueError:
                print(Fore.RED + "Некоректнный ввод")

            pressEnter()

        elif com == 'i':
            return

def pressEnter():
    input(Fore.CYAN + "Press enter...")

def main():
    interface()

main()