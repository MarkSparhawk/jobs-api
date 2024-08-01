# Code based on flask CRUD tutorial here
# https://medium.com/@hillarywando/how-to-create-a-basic-crud-api-using-python-flask-cd68ef5fd7e3

import sqlite3, random, datetime
from models import Job


def getNewId():
    return random.getrandbits(28)


jobs = [
    {
        'company': 'Microsoft',
        'title': 'Senior Site Reliability Engineer',
        'url': 'https://www.linkedin.com/jobs/view/3984242407',
        'recruiter': 'Jack Sparrow',
        'timestamp': datetime.datetime.now()
    },
    {
        'company': 'LinkedIn',
        'title': 'Principal Staff Software Engineer',
        'url': 'https://www.linkedin.com/jobs/view/3958836337',
        'recruiter': 'Elizabeth Swann',
        'timestamp': datetime.datetime.now()
    },
    {
        'company': 'Meta',
        'title': 'Software Engineer, iOS',
        'url': 'https://www.metacareers.com/jobs/1581240112368193/',
        'recruiter': 'Davy Jones',
        'timestamp': datetime.datetime.now()
    },
]    

def connect():
    conn = sqlite3.connect('jobs.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, company TEXT, title TEXT, url TEXT, recruiter TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()
    for i in jobs:
        jb = Job(getNewId(), i['company'], i['title'], i['url'], i['recruiter'], i['timestamp'])
        insert(jb)

def insert(job):
    conn = sqlite3.connect('jobs.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO jobs VALUES (?,?,?,?,?,?)", (
        job.id,
        job.company,
        job.title,
        job.url,
        job.recruiter,
        job.timestamp
    ))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('jobs.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs")
    rows = cur.fetchall()
    jobs = []
    for i in rows:
        job = Job(i[0], i[1], i[2], i[3], i[4], i[5])
        jobs.append(job)
    conn.close()
    return jobs

def update(job):
    conn = sqlite3.connect('jobs.db')
    cur = conn.cursor()
    cur.execute("UPDATE jobs SET company=?, title=?, url=?, recruiter=? WHERE id=?", (job.company, job.title, job.url, job.recruiter, job.id))
    conn.commit()
    conn.close()

def delete(theId):
    conn = sqlite3.connect('jobs.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM jobs WHERE id=?", (theId,))
    conn.commit()
    conn.close()

def deleteAll():
    conn = sqlite3.connect('jobs.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM jobs")
    conn.commit()
    conn.close()