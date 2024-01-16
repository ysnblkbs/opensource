from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')

        bins = [0, 18, 30, 50, 100]
        labels = ['Child', 'Young', 'Middle-aged', 'Elderly']
        data['Classification'] = pd.cut(data['age'], bins=bins, labels=labels)

        result = data[['name', 'age', 'city', 'Classification']].to_dict('records')
        return {'data' : result}, 200

    def post(self):
        name = request.args['name']
        age  = request.args['age']
        city = request.args['city']
        req_data = pd.DataFrame({
            'name'      : [name],
            'age'       : [age],
            'city'      : [city]
        })
        data = pd.read_csv('users.csv')
        data = data.append(req_data, ignore_index=True)
        data.to_csv('users.csv', index=False)
        return {'message' : 'Record successfully added.'}, 200

class Name(Resource):
    def get(self,name):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name :
                return {'data' : entry}, 200
        return {'message' : f"No entry found with this name: {name}."}, 404

class Cities(Resource):
    def get(self):
        data = pd.read_csv('users.csv',usecols=[2])
        data = data.to_dict('records')
        return {'data' : data}, 200

api.add_resource(Users, '/users')
api.add_resource(Cities, '/cities')
api.add_resource(Name, '/users/<string:name>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    app.run()

