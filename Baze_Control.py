import sqlite3


def start():
    try:
        # print("Work")
        conn = sqlite3.connect("Base.bd")
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_iD INTEGER NOT NULL UNIQUE, join_date DATETIME NOT NULL DEFAULT( (DATETIME('now')) ))")
        conn.commit()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS lern (id INTEGER PRIMARY KEY AUTOINCREMENT, user_iD INTEGER NOT NULL, add_time DATETIME NOT NULL DEFAULT((   DATETIME('now'))), progress INTEGER, type TEXT, matereal TEXT)")
        conn.commit()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS lerned (id INTEGER PRIMARY KEY AUTOINCREMENT, user_iD INTEGER NOT NULL, add_time DATETIME NOT NULL DEFAULT((DATETIME('now'))), type TEXT, matereal TEXT)")
        conn.commit()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS archive (id INTEGER PRIMARY KEY AUTOINCREMENT, user_iD INTEGER NOT NULL , type TEXT, matereal TEXT)")
        conn.commit()
        # print("Work 2")
    except sqlite3.Error as er:

        print(f'SQLITE3 ERROR form start: {er}')

    finally:
        if conn:
            cur.close()
            conn.close()


def add_user(user_id):
    try:
        print("add_user1")
        conn = sqlite3.connect("Base.bd")
        cur = conn.cursor()
        print("add_user2")
        cur.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES(?)", (user_id,))
        conn.commit()
        print("add_user3")
        cur.execute("SELECT * FROM 'users'")
        fetch = cur.fetchall()
        print("add_user4")
        print(fetch)
    except sqlite3.Error as er:
        print(f'SQLITE3 ERROR from add_user: {er}')

    finally:
        if conn:
            cur.close()
            conn.close()


def read_base(user_id, name_base):
    try:
        conn = sqlite3.connect("Base.bd")
        cur = conn.cursor()
        print("\nData from read_base: user_id:", user_id, "name_base:", name_base, )
        '''
        user = read_base(user_id, 'users')
        if len(user) != 1:
            print("In read_base Error, len(user) != 1 ", len(user), user_id)
            return (False)
        id_user = user[0]

        if name_base == "users":
            id_user = user_id
        '''
        cur.execute(f"SELECT * FROM {name_base}")
        fetch = cur.fetchall()
        sort_list = list()
        for i in fetch:
            if i[1] == user_id:
                sort_list.append(i)

        print("List from read_base:", fetch, "\nSorted_list from read_base:", sort_list)
        return (sort_list)
        print("\n")
    except sqlite3.Error as er:
        print(f'SQLITE3 ERROR from read_base: {er}')
    # finally:
    #    if conn:
    #        cur.close()
    #        conn.close()


def add_lern(user_id, type, matereal, progress_mat):
    try:
        conn = sqlite3.connect("Base.bd")
        cur = conn.cursor()
        user = read_base(user_id, 'users')
        if len(user) != 1:
            print("In add_lern Error, len(user) != 1 ", len(user), user_id, type, matereal, progress_mat)
            return (False)
        id_user = user[0]
        print(f"add_lern data: user_id: {user_id} , type: {type} , matereal: {matereal}, progress_mat: {progress_mat}")
        matereal = str(matereal)
        type = str(type)
        id_user = int(id_user[0])
        progress_mat = int(progress_mat)
        cur.execute("INSERT INTO 'lern' ('user_id', 'progress', 'type', 'matereal') VALUES(?,?,?,?)",
                    (id_user, progress_mat, type, matereal))
        conn.commit()
    except sqlite3.Error as er:
        print(f'SQLITE3 ERROR from add_lern: {er}')

    finally:
        if conn:
            cur.close()
            conn.close()


def add_lerned(user_id, record_num):
    # print('in work)')
    try:

        print(f"\nData from add_lerned: user_id: {user_id}, record_num: {record_num}\n")
        conn = sqlite3.connect("Base.bd")
        cur = conn.cursor()
        user = read_base(user_id, 'users')
        if len(user) != 1:
            print(len(user), user_id)
            return (False)
        id_user = user[0][0]
        lern_list = read_base(id_user, "lern")
        mat = lern_list[record_num]

        # перепеши на добавление именно сюды, пока это просто lern
        cur.execute("INSERT INTO 'lerned' ('user_id', 'type', 'matereal') VALUES(?,?,?)", (id_user, mat[4], mat[5]))
        conn.commit()
    except sqlite3.Error as er:

        print(f'SQLITE3 ERROR from add_lerned: {er}')

    finally:
        if conn:
            cur.close()
            conn.close()


def add_archive(user_id, record_num):
    # print('in work)')
    try:

        print(f"\nData from add_archive: user_id: {user_id}, record_num: {record_num}\n")
        conn = sqlite3.connect("Base.bd")
        cur = conn.cursor()
        user = read_base(user_id, 'users')
        if len(user) != 1:
            print(len(user), user_id)
            return (False)
        id_user = user[0][0]
        lern_list = read_base(id_user, "lern")
        mat = lern_list[record_num]

        # перепеши на добавление именно сюды, пока это просто lern
        cur.execute("INSERT INTO 'archive' ('user_id', 'type', 'matereal') VALUES(?,?,?)", (id_user, mat[4], mat[5]))
        conn.commit()
    except sqlite3.Error as er:

        print(f'SQLITE3 ERROR from add_archive: {er}')

    finally:
        if conn:
            cur.close()
            conn.close()


def remove(id, base):
    try:
        id += 1
        print(f"\nData from remove: id: {id}, base: {base}\n")
        conn = sqlite3.connect("Base.bd")
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {base} WHERE id == {id}")
        conn.commit()

    except sqlite3.Error as er:
        print(f'SQLITE3 ERROR from remove: {er}')
    finally:
        if conn:
            cur.close()
            conn.close()
