import psycopg2
from dataclasses import dataclass
from colorama import init, Fore
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

def getDiscipline(course_number):
    conn = getConn()

    if conn is None:
        print(Fore.RED + "Ошибка подключения")
        return
    
    cur = conn.cursor()
    cur.execute("SELECT name FROM disciplines WHERE course_num = %s", (course_number, ))
    discipline = cur.fetchall()

    print(Fore.GREEN + f"Занятия {course_number} курса: {discipline}")
        