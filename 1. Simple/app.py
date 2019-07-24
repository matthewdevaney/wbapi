from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api (app)

countriesList = [
    {
        'name': 'Canada',
        'code': 'CAN',
        'region': 'North America',
        'population': 37058856,
    },
    {
        'name': 'United States',
        'code': 'USA',
        'region': 'North America',
        'population': 327167434,
    },
    {
        'name': 'Mexico',
        'code': 'MEX',
        'region': 'Latin America & Caribbean',
        'population': 126190788,
    }
]

class Country(Resource):
    
    def get(self):
    # get the data for a country with a matching country code

        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args()

        for country in countriesList:
            if country['code'] == args['code']:
                return country, 200
        
        return 'Country not found!', 404

    def post(self):
    # create a new country
    
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('code', type=str, required=True)
        parser.add_argument('region', type=str)
        parser.add_argument('population', type=int)
        args = parser.parse_args()

        for country in countriesList:
            if country['code'] == args['code']:
                return f"Error: Country with code {country['code']} already exists", 400

        new_country = {
            'name': args['name'],
            'code': args['code'],
            'region': args['region'],
            'population': args['population']
        }

        countriesList.append(new_country)
        return f"Success: {new_country['name']} was added to the list" , 200

    def put(self):
    # update the data of an existing country with the matching country code

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('code')
        parser.add_argument('region', type=str)
        parser.add_argument('population', type=int)
        args = parser.parse_args()

        for country in countriesList:
            if country['code'] == args['code']:
                country['name'] = args['name']
                country['region'] = args['region']
                country['population'] = args['population']
                return f"Success: Country with code {country['code']} was updated", 200
        
        return f"Error: Country with code {args['code']} could not be found", 400


    def delete(self):

        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args()

        for country in countriesList:
            if country['code'] == args['code']:
                countriesList.remove(country)
                return f"Success: Country with code {country['code']} was removed", 200
        
        return f"Error: Country with code {args['code']} could not be found", 400

api.add_resource(Country, '/api/countries')


if __name__ == '__main__':
    app.run(debug=True)