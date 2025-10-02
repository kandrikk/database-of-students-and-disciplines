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
        print(Fore.RED + "Ошибка подключения.")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id = %s", (id, ))
    student = cur.fetchone()

    if student:
        print(Fore.GREEN + f"\nСтудент найден.")
        print(f"Имя: {student[1]} \nНомер курса: {student[2]}")
    else:
        print(Fore.YELLOW + "Студента с данным ID не существует.")

    cur.close()
    conn.close()

def getDiscipline(course):
    if course > 8 or course < 1:
        print(Fore.YELLOW + f"Некорректные данные номера курса.")
        return

    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения.")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT discipline_name, day, pair_number FROM disciplines WHERE course = %s ORDER BY day, pair_number"
                , (course,))
    
    check = cur.fetchall()
    if not check:
        print(Fore.YELLOW + f"Занятий на {course} курсе нет.")
        cur.close()
        conn.close()
        return
    
    day_week = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    
    for day in day_week:
        cur.scroll(0, mode='absolute')
        
        day_disciplines = [(pair_number, name) for name, d, pair_number in cur.fetchall() if d == day]
        
        print(Fore.GREEN + f"\n{day.capitalize()}:" if day_disciplines else Fore.YELLOW + f"\n{day.capitalize()}:")
        
        for pair_number, name in day_disciplines:
            print(f"  {pair_number}. {name}")
        
        if not day_disciplines:
            print("  занятий нет")

    cur.close()
    conn.close()

def getStudents(course):
    if course > 8 or course < 1:
        print(Fore.YELLOW + f"Курса по {course} не существует.")
        return

    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения.")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT name FROM students WHERE course = %s ORDER BY name", (course,))
    
    students = cur.fetchall()
    
    if students:
        print(Fore.GREEN + f"Студенты {course} курса:")
        for student in students:
            print(f"  - {student[0]}")
    else:
        print(Fore.YELLOW + f"На курсе {course} студентов не найдено.")
    
    cur.close()
    conn.close()

def getDisciplines():
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения.")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM disciplines ORDER BY id")
    disciplines = cur.fetchall()

    if not disciplines:
        print(Fore.YELLOW + "Расписание дисциплин пустое.")
        return

    print(Fore.CYAN + "(ID, Название дисциплины, День недели, Номер пары, Номер курса)")
    for disc in disciplines:
        print(disc)
    
    cur.close()
    conn.close()

def putStudent(name, course):
    if name == '' or course < 1 or course > 8:
        print(Fore.RED + "Некорректные данные.")
        return
        
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения.")
        return
    
    cur = conn.cursor()
    
    try:
        cur.execute("INSERT INTO students (name, course) VALUES (%s, %s)", (name, course))
        conn.commit()
        print(Fore.GREEN + f"Студент {name} успешно добавлен на курс {course}")
    except psycopg2.Error as e:
        print(Fore.RED + f"Ошибка при добавлении студента: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def putDiscipline(name, day, pair_number, course):
    day_week = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

    day = day.strip().lower()

    if (name == '') or (day not in day_week) or (pair_number > 9) or (pair_number < 1) or (course > 8) or (course < 1):
        print(Fore.RED + "Некорректные данные.")
        return

    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения.")
        return
    
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM disciplines WHERE day = %s AND pair_number = %s AND course = %s"
                    , (day, pair_number, course))
        
        disc = cur.fetchone()

        if disc:
            print(Fore.YELLOW + "Занятие с такими параметрами имеется в расписание.")
            return

        cur.execute("INSERT INTO disciplines (discipline_name, day, pair_number, course) VALUES (%s, %s, %s, %s)"
                    , (name, day, pair_number, course))
        conn.commit()
        print(Fore.GREEN + f"Дисциплина успешно добавлена.")
    except psycopg2.Error as e:
        print(Fore.RED + f"Ошибка при добавлении дисциплина: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def deleteStudent(id):
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения.")
        return
    
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE id = %s", (id, ))
    st = cur.fetchone()
    if not st:
        print(Fore.YELLOW + "Студента с данным ID не существует.")
        cur.close()
        conn.close()
        return

    try:
        cur.execute("DELETE FROM students WHERE id = %s", (id, ))
        conn.commit()
        print(Fore.GREEN + f"Студент с ID {id} удален.")
    except psycopg2.Error as e:
        print(Fore.RED + f"Ошибка при удаление студента: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def deleteDiscipline(id):
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения.")
        return
    
    cur = conn.cursor()

    cur.execute("SELECT * FROM disciplines WHERE id = %s", (id, ))
    dn = cur.fetchone()
    if not dn:
        print(Fore.YELLOW + "Занятия с данным ID не существует.")
        cur.close()
        conn.close()
        return

    try:
        cur.execute("DELETE FROM disciplines WHERE id = %s", (id, ))
        conn.commit()
        print(Fore.GREEN + f"Занятие с ID {id} удалено.")
    except psycopg2.Error as e:
        print(Fore.RED + f"Ошибка при удаление занятия: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def getAllStudents():
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения.")
        return
    
    cur = conn.cursor()

    cur.execute("SELECT * FROM students ORDER BY id")

    students = cur.fetchall()
    if not students:
        print(Fore.YELLOW + "Хранилище студентов пустое.")
        cur.close()
        conn.close()
        return
    
    print(Fore.CYAN + "(ID, Имя студента, Номер курса)")
    for stud in students:
        print(stud)
    
    cur.close()
    conn.close()

    
def getDisciplineId(id):
    conn = getConn()
    if not conn:
        print(Fore.RED + "Ошибка подключения.")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM disciplines WHERE id = %s", (id, ))
    disc = cur.fetchone()

    if disc:
        print(Fore.GREEN + f"\nЗанятие найдено.")
        print(f"Название дисциплины: {disc[1]} \nДень: {disc[2]} \nНомер пары: {disc[3]} \nНомер курса: {disc[4]}")
    else:
        print(Fore.YELLOW + "Занятия с данным ID не существует.")

    cur.close()
    conn.close()


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

    varib = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'i']
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
                id = int(input("Введите ID студента: "))
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
                day = input("Введите день занятия: ")
                pair_number = int(input("Введите номер пары: "))
                course = int(input("Введите номер курса: "))

                putDiscipline(name, day, pair_number, course)
            except ValueError:
                print(Fore.RED + "Некоректнный ввод.")

            pressEnter()

        elif com == 'g':
            try:
                id = int(input("Введите ID: "))
                deleteStudent(id)
                
            except ValueError:
                print(Fore.RED + "Некоректнный ввод.")

            pressEnter()

        elif com == 'h':
            try:
                id = int(input("Введите ID: "))
                deleteDiscipline(id)
                
            except ValueError:
                print(Fore.RED + "Некоректнный ввод.")

            pressEnter()

        elif com == 'j':
            getAllStudents()

            pressEnter()

        elif com == 'k':
            try:
                id = int(input("Введите ID: "))
                getDisciplineId(id)
            except ValueError:
                print(Fore.RED + "Некоректнный ввод.")

            pressEnter()

        elif com == 'i':
            return

def pressEnter():
    input(Fore.CYAN + "Press enter...")
    print("\n\n\n")

def main():
    interface()

main()