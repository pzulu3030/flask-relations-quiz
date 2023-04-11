from flask import Flask, jsonify
from api.lib.orm import find_all, build_from_record, build_from_records, find
from api.lib.db import get_db
from api.models import Person

import json
import psycopg2

def create_app(db_name):
    app = Flask(__name__)
    app.config.from_mapping(DATABASE = db_name)
    
    @app.route('/')
    def root_url():
        return 'welcome to the imdb movies app'
    
    @app.route('/persons')
    def persons():
        conn = get_db()

        cursor = conn.cursor()
        persons = find_all(Person, cursor, 5)

        persons_dicts = [person.__dict__ for person in persons]
        breakpoint()
        return json.dumps(persons_dicts,default = str)

    @app.route('/persons/lastname')
    def showlastname():
        pass
    
    return app
