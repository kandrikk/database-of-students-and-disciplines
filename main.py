from colorama import Fore, init
import psycopg2

init(autoreset=True)

MAX_COURSE = 8
MIN_COURSE = 1
MAX_PAIR_NUMBER = 9
MIN_PAIR_NUMBER = 1
MAX_NAME_LEN = 255
MIN_NAME_LEN = 1
DAY_WEEK = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']

def getConn():
    try:
        conn = psycopg2.connect(dbname='study', user='postgres',
                                password='postgres', host='localhost',
                                port=5432)
        
        return conn
    except psycopg2.Error:
        return None

def db_conn(fn):
    def template(*args, **params):
        conn = None
        try:
            conn = getConn()
            if not conn:
                print(Fore.RED + "Ошибка подключения.\nПроверьте работу базы данных.")
                return

            with conn.cursor() as cur:
                return fn(cur, *args, **params)
            
        finally:
            if conn:
                conn.close()
        
    return template

def db_conn_and_commit(fn):
    def template(*args, **params):
        conn = None
        try:
            conn = getConn()
            if not conn:
                print(Fore.RED + "Ошибка подключения.\nПроверьте работу базы данных.")
                return

            with conn.cursor() as cur:
                result = fn(cur, *args, **params)
                conn.commit()
                return result
            
        except Exception as e:
            print(Fore.RED + f"Ошибка: {e}")
            if conn:
                conn.rollback()
            
        finally:
            if conn:
                conn.close()
        
    return template

        
@db_conn
def getStudent(cur, id):
    cur.execute("""SELECT * FROM students 
                WHERE id = %s"""
                , (id, ))
    
    student = cur.fetchone()

    if student:
        print(Fore.GREEN + f"\nСтудент найден.")
        print(f"Имя: {student[1]} \nНомер курса: {student[2]}")
    else:
        print(Fore.YELLOW + "Студента с данным ID не существует.")

@db_conn
def getDiscipline(cur, course):
    if course > MAX_COURSE or course < MIN_COURSE:
        print(Fore.YELLOW + f"{course} курса не существует.")
        return

    cur.execute("""SELECT discipline_name, day, pair_number 
                FROM disciplines 
                WHERE course = %s 
                ORDER BY day, pair_number"""
                , (course,))
    
    all_disciplines = cur.fetchall()
    if not all_disciplines:
        print(Fore.YELLOW + f"Занятий на {course} курсе нет.")
        return
    
    for day in DAY_WEEK:
        day_disciplines = []
        for name, d, pair_number in all_disciplines:
            if d == day:
                day_disciplines.append((pair_number, name))
        
        if day_disciplines:
            print(Fore.GREEN + f"\n{day.capitalize()}:")
            for pair_number, name in day_disciplines:
                print(f"  {pair_number}. {name}")

        else: 
            print(Fore.YELLOW + f"\n{day.capitalize()}:")
            print("  занятий нет")

@db_conn
def getStudents(cur, course):
    if course > MAX_COURSE or course < MIN_COURSE:
        print(Fore.YELLOW + f"{course} курса не существует.")
        return
    
    cur.execute("""SELECT name FROM students 
                WHERE course = %s 
                ORDER BY name"""
                , (course,))
    
    students = cur.fetchall()
    
    if students:
        print(Fore.GREEN + f"Студенты {course} курса:")
        for student in students:
            print(f"  - {student[0]}")
    else:
        print(Fore.YELLOW + f"На курсе {course} студентов не найдено.")

@db_conn
def getDisciplines(cur):
    cur.execute("""SELECT * FROM disciplines 
                ORDER BY id""")
    
    disciplines = cur.fetchall()

    if not disciplines:
        print(Fore.YELLOW + "Расписание дисциплин пустое.")
        return

    print(Fore.CYAN + "(ID, Название дисциплины, День недели, Номер пары, Номер курса)")
    for disc in disciplines:
        print(disc)

@db_conn_and_commit
def putStudent(cur, name, course):
    name = name.strip()

    valid = (
        MIN_NAME_LEN <= len(name) <= MAX_NAME_LEN and
        MIN_COURSE <= course <= MAX_COURSE
    )

    if not valid:
        print(Fore.RED + "Некорректные данные.")
        return
    
    cur.execute("""INSERT INTO students (name, course)
                VALUES (%s, %s)"""
                , (name, course))
    

    print(Fore.GREEN + f"Студент {name} успешно добавлен на курс {course}")

@db_conn_and_commit
def putDiscipline(cur, name, day, pair_number, course):
    name = name.strip()
    day = day.strip().lower()

    valid = (
        MIN_NAME_LEN <= len(name) <= MAX_NAME_LEN and
        day in DAY_WEEK and
        MIN_COURSE <= course <= MAX_COURSE and
        MIN_PAIR_NUMBER <= pair_number <= MAX_PAIR_NUMBER
    )

    if not valid:
        print(Fore.RED + "Некорректные данные.")
        return

    cur.execute("""SELECT * FROM disciplines 
                WHERE day = %s AND pair_number = %s AND course = %s"""
                , (day, pair_number, course))
    
    disc = cur.fetchone()

    if disc:
        print(Fore.YELLOW + "Занятие с такими параметрами имеется в расписании.")
        return

    cur.execute("""INSERT INTO disciplines (discipline_name, day, pair_number, course)
                VALUES (%s, %s, %s, %s)"""
                , (name, day, pair_number, course))
        
    print(Fore.GREEN + f"Дисциплина успешно добавлена.")

@db_conn_and_commit
def deleteStudent(cur, id):
    cur.execute("""SELECT * FROM students 
                WHERE id = %s"""
                , (id, ))
    
    student = cur.fetchone()
    if not student:
        print(Fore.YELLOW + "Студента с данным ID не существует.")
        return

    cur.execute("""DELETE FROM students 
                WHERE id = %s"""
                , (id, ))

    print(Fore.GREEN + f"Студент с ID {id} удален.")


@db_conn_and_commit
def deleteDiscipline(cur, id):
    cur.execute("""SELECT * FROM disciplines 
                WHERE id = %s"""
                , (id, ))
    
    discipline = cur.fetchone()
    if not discipline:
        print(Fore.YELLOW + "Занятия с данным ID не существует.")
        return

    cur.execute("""DELETE FROM disciplines 
                WHERE id = %s"""
                , (id, ))
    
    print(Fore.GREEN + f"Занятие с ID {id} удалено.")


@db_conn
def getAllStudents(cur):
    cur.execute("""SELECT * FROM students 
                ORDER BY id""")

    students = cur.fetchall()
    if not students:
        print(Fore.YELLOW + "Хранилище студентов пустое.")
        return
    
    print(Fore.CYAN + "(ID, Имя студента, Номер курса)")
    for stud in students:
        print(stud)

@db_conn
def getDisciplineId(cur, id):
    cur.execute("""SELECT * FROM disciplines 
                WHERE id = %s"""
                , (id, ))
    
    disc = cur.fetchone()

    if disc:
        print(Fore.GREEN + f"\nЗанятие найдено.")
        print(f"Название дисциплины: {disc[1]} \nДень: {disc[2]} \nНомер пары: {disc[3]} \nНомер курса: {disc[4]}")
    else:
        print(Fore.YELLOW + "Занятия с данным ID не существует.")


def menu():
    print(Fore.GREEN + "   Выберите команду")
    print("a. Найти студента по ID.")
    print("b. Все занятия по номеру курса.")
    print("c. Список всех студентов по номеру курса.")
    print("d. Полное расписание дисциплин.")
    print("e. Добавить нового студента.")
    print("f. Добавить занятия в расписание.")
    print("g. Удаление студента по ID.")
    print("h. Удаление занятия по ID.")
    print("j. Список всех студентов.")
    print("k. Найти занятие по ID.")
    print("i. Выйти.")

def interface():
    while True:
        menu()
        command = input("\nВведите команду: ")

        try:
            if command == 'a':
                id = int(input("Введите ID студента: "))
                getStudent(id)

            elif command == 'b':
                num = int(input("Введите номер курса: "))
                getDiscipline(num)

            elif command == 'c':
                num = int(input("Введите номер курса: "))
                getStudents(num)

            elif command == 'd':
                getDisciplines()

            elif command == 'e':
                name = input("Введите имя студента: ")
                num_course = int(input("Введите номер курса: "))
                putStudent(name, num_course)

            elif command == 'f':
                name = input("Введите название дисциплины: ")
                day = input("Введите день занятия: ")
                pair_number = int(input("Введите номер пары: "))
                course = int(input("Введите номер курса: "))

                putDiscipline(name, day, pair_number, course)

            elif command == 'g':
                id = int(input("Введите ID: "))
                deleteStudent(id)

            elif command == 'h':
                id = int(input("Введите ID: "))
                deleteDiscipline(id)

            elif command == 'j':
                getAllStudents()

            elif command == 'k':
                id = int(input("Введите ID: "))
                getDisciplineId(id)

            elif command == 'i':
                return
            
            else:
                print(Fore.RED + "Некорректный ввод.")

            
        except ValueError:
            print(Fore.RED + "Некорректный ввод.")
            
        finally:
            if command == '' or command not in 'i':
                pressEnter()

def pressEnter():
    input(Fore.CYAN + "Press enter...")
    print("\n\n\n")

def main():
    interface()

main()