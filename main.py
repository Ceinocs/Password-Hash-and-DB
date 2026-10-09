import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidKey
import sqlite3
import csv

conn = sqlite3.connect('database.db')
cursor = conn.cursor()


cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT UNIQUE, 
        hash_password BLOB,
        salt BLOB
    )
'''
)

conn.commit()

def hash_password(password: str) -> tuple[bytes,bytes]:
    pas_bytes = password.encode('utf-8')
    salt = os.urandom(16)
    kdf = Scrypt(salt = salt, length=32, n = 2**14, r = 8, p = 1)
    hash_pass = kdf.derive(pas_bytes)
    return hash_pass, salt

def verify_hash_password(password: str, hash_pass: bytes, salt: bytes) -> bool:
    pas_bytes = password.encode('utf-8')
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)
    try:
        kdf.verify(pas_bytes,hash_pass)
        return True
    except InvalidKey:
        return False


def start():
    ans = str(input('Войти - (1) или за регистрироваться - (2): ').strip())
    if ans == '1':
        sigin()
    elif ans == '2':
        sigan()
    else:
        print("Неверный ввод. Попробуйте еще раз.")
        start()

def sigin():
    print('\nПривет бывалый! :)')
    name = str(input('введите имя: ').strip())

    cursor.execute('SELECT hash_password, salt FROM users WHERE name = ?', (name,) )
    user = cursor.fetchone()
    if user:
        hs_val = user[0]
        salt_val = user[1]
        password = str(input('введите пароль: ').strip())
        if verify_hash_password(password,hs_val,salt_val):
            entrance(name)
        else:
            error_has_user()
    else:
        error_has_user()


def sigan():
    print('\nПривет новичек! :)')
    name = str(input('введите имя: ').strip())

    cursor.execute("SELECT id FROM users WHERE name = ?", (name,))
    if cursor.fetchone():
        print("Такое имя уже есть. :( \nВыбери другое или же войди.")
        start()
        return

    password = str(input('введите пароль: ').strip())
    hs_val, salt_val = hash_password(password)
    cursor.execute('INSERT INTO users (name,hash_password,salt) VALUES (?, ?,?)', (name,hs_val,salt_val))
    conn.commit()
    entrance(name)

def export_to_excel():
    cursor.execute("SELECT id, name, hash_password, salt FROM users")
    rows = cursor.fetchall()
    with open('users_backup.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['ID', 'Username', 'Password Hash', 'Salt'])
        writer.writerows(rows)

def entrance(name):
    print(f'\nДобро пожаловать {name}')
    export_to_excel()


#Error
def examination():
    print('Попробовать еще - (1) или создать новый аккаунт - (2) ??:')
    ans = str(input().strip())
    if ans == '1':
        sigin()
    elif ans == '2':
        sigan()
    else:
        print('Чуваааак!!!! ты написал вобше не то :(')
        examination()


def error_has_user():
    print('\nБлин чувак не тот пароль или имя давай еше раз ')
    examination()




def error_name_and_name():
    print('\nБлин ошбыбочка в имени проверь!')
    sigin()



if __name__ == '__main__':
    try:
        start()
    finally:
        # Закрываем соединение при выходе из программы
        cursor.close()
        conn.close()