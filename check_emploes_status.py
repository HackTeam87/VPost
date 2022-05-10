from db.connect_db import SessionLocal


db = SessionLocal()

def emploe_status():
    #Делаем выборку с табеля учета рабочего времени
    query = f'''
    SELECT emploe_id, work_day_count
    FROM time_sheets
    '''
    r = db.execute(query)
    
    L = []
    for i in r:
        L.append({'emploe_id': i[0], 'work_day_count': i[1]})
    for s in L: 
        e_id = s['emploe_id']
        if (s['work_day_count'] % 2) == 0:
            db.execute(f'UPDATE employees SET status=0 WHERE id={e_id}')
            print ('status: Выходной') 
        else:
            db.execute(f'UPDATE employees SET status=1 WHERE id={e_id}')
            print ('status: В работе') 
    #Определяем статус работника и записываем в базу
    #Скрипт надо добавить в Cron :
    # 00    00    *    *    *  ./PostBot/check_emploes_status.py
    db.commit()        
emploe_status()

                         
    