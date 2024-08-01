# Code based on flask CRUD tutorial here
# https://medium.com/@hillarywando/how-to-create-a-basic-crud-api-using-python-flask-cd68ef5fd7e3

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os, datetime
import db
from models import Job

app = Flask(__name__)
CORS(app)

# create the database and table. Insert test jobs into db
if not os.path.isfile('jobs.db'):
    db.connect()

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/jobs', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    jobs = [j.serialize() for j in db.view()]
    if (content_type == 'application/json'):
        json = request.json
        for j in jobs:
            if j['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': j,
                    'status': '200',
                    'msg': 'Success getting all jobs'
                })
        return jsonify({
            'error': f"Error: Job with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': jobs,
                    'status': '200',
                    'msg': 'Success getting all jobs',
                    'no_of_jobs': len(jobs)
                })


@app.route("/jobs", methods=['POST'])
def postRequest():
    req_data = request.get_json()
    company = req_data['company']
    url = req_data['url']
    title = req_data['title']
    recruiter = req_data['recruiter']

    jobs = [j.serialize() for j in db.view()]
    for j in jobs:
        if j['company'] == company:
            return jsonify({
                # 'error': '',
                'res': f'Error: Job with company {company} already exists!',
                'status': '404'
            })

    job = Job(db.getNewId(), company, title, url, recruiter, datetime.datetime.now())
    print('new job: ', job.serialize())
    db.insert(job)
    new_jobs = [j.serialize() for j in db.view()]
    print('jobs in account: ', new_jobs)
    
    return jsonify({
                # 'error': '',
                'res': job.serialize(),
                'status': '200',
                'msg': 'Success creating a new job!'
            })



@app.route('/jobs/<id>', methods=['GET'])
def getRequestId(id):
    req_args = request.view_args
    # print('req_args: ', req_args)
    jobs = [j.serialize() for j in db.view()]
    if req_args:
        for j in jobs:
            if j['id'] == int(req_args['id']):
                return jsonify({
                    # 'error': '',
                    'res': j,
                    'status': '200',
                    'msg': 'Success getting job by ID!'
                })
        return jsonify({
            'error': f"Error: Job with id '{req_args['id']}' was not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': jobs,
                    'status': '200',
                    'msg': 'Success getting job by ID!',
                    'no_of_jobs': len(jobs)
                })


@app.route('/jobs/<id>', methods=['DELETE'])
def deleteRequest(id):
    req_args = request.view_args
    print('req_args: ', req_args)
    jobs = [j.serialize() for j in db.view()]
    if req_args:
        for job in jobs:
            if job['id'] == int(req_args['id']):
                db.delete(job['id'])
                updated_jobs = [j.serialize() for j in db.view()]
                print('updated_jobs: ', updated_jobs)
                return jsonify({
                    'res': updated_jobs,
                    'status': '200',
                    'msg': 'Success deleting job by ID',
                    'no_of_books': len(updated_jobs)
                })
    else:
        return jsonify({
            'error': f"Error: No Job ID sent!",
            'res': '',
            'status': '404'
        })

@app.route("/jobs/<id>", methods=['PUT'])
def putRequest(id):
    req_data = request.get_json()
    company = req_data['company']
    url = req_data['url']
    title = req_data['title']
    recruiter = req_data['recruiter']
    jobs = [j.serialize() for j in db.view()]
    for j in jobs:
        if str(j['id']) == id:
            job = Job(
                id, 
                company,
                title,
                url,
                recruiter,
                datetime.datetime.now()
            )
            print('new job: ', job.serialize())
            db.update(job)
            new_jobs = [j.serialize() for j in db.view()]
            print('jobs in lib: ', new_jobs)
            return jsonify({
                # 'error': '',
                'res': job.serialize(),
                'status': '200',
                'msg': f'Success updating the job {title} for {company}!'
            })        
    return jsonify({
                # 'error': '',
                'res': f'Error: Failed to update job {title} for {company} with id={id}!',
                'status': '404'
            })
    

if __name__ == '__main__':
    app.run()