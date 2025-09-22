#crawl the graph of users and save to a sql database
import os
import numpy as np
import requests
from itertools import islice
import sqlite3
import time

api_calls=0
def get_following(user):
    global api_calls
    try:
        x=0
        following=[]
        while True:
            api_calls+=1
            response=requests.get("https://api.scratch.mit.edu/users/"+user+"/following/?limit=40&offset="+str(x))
            if len(response.json())==0 or response.status_code==404:
                break
            try:
                for i in response.json():
                    following.append((i['username']))
            except:
                pass
            x+=40
        return following
    except:
        print("get following error with "+ user)
        return []

def load_file(filename, n, m): #return the lines n-m of a file (0-indexed, n inclusive, m non-inclusive)    
    with open(filename, 'r') as f:
        lines = [line.strip() for line in islice(f, n, m)]
    array=np.array(lines)
    f.close()
    return array

def add_to_file(filename, lines): #add lines to the file
    with open(filename, "a") as f:
        for line in lines:
            f.write(line + "\n")
    f.close()

def delete_from_file(filename, n): #delete the first n lines from the file
    temp_filename = "data_temp.txt"

    with open(filename, 'r') as src, open(temp_filename, 'w') as dst:
        for i, line in enumerate(src):
            if i >= n:
                dst.write(line)

    os.replace(temp_filename, filename)


def main():
    global api_calls
    start=time.time()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("PRAGMA synchronous = NORMAL;")

    queue=load_file("queue.txt",0,100)
    queue_new=[]
    print("NEW CYCLE: ")

    long=0
    api_calls=0
    with conn:
        for user in queue:
            following = get_following(user)
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (user,))
            source_id = cursor.fetchone()[0]
            for user2 in following:
                cursor.execute("SELECT user_id FROM users WHERE username = ?", (user2,))
                result = cursor.fetchone()
                if result==None:
                    cursor.execute("INSERT INTO users (username) VALUES (?)", (user2,))
                    queue_new.append(user2)
                    target_id = cursor.lastrowid
                else:
                    target_id=result[0]
                    pass
                cursor.execute("INSERT OR IGNORE INTO edges (source_id, target_id) VALUES (?,?)", (source_id, target_id))
        
    #finalise changes:
    print(str(len(queue_new))+" users added to the queue.")

    add_to_file("queue.txt", queue_new)
    delete_from_file("queue.txt", len(queue))

    conn.commit()
    
    end=time.time()
    print("changes finalised. time elapsed: "+str(end-start)+". api calls: "+str(api_calls))

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);")
conn.commit()
conn.close()
while True:
    main()
