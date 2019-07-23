# 1. Explain REST API and Simple CRUD
# 2. GET multiple arguments, multiple results, marshalling
# 3. Authentication
# 4. Creating a database w/ model, webapp
# 5. Deployment

from flask import Flask
from flask_restful import Resource, Api, reqparse, fields, marshal
import json

app = Flask(__name__)
api = Api(app)

countriesList = [
    {
        'Name': 'Argentina',
        'code': 'ARG',
        'region': 'Latin America Caribbean',
        'population': 44494502,
        'land area': 2736690,
        'density': 16
    },
    {
        'name': 'Brazil',
        'code': 'BRA',
        'region': 'Latin America Caribbean',
        'population': 209469333,
        'land area': 8358140,
        'Density': 25
    },
    {
        'name': 'Canada',
        'code': 'CAN',
        'region': 'North America',
        'population': 37058856,
        'land area': 9093510,
        'density': 4
    },
    {
        'name': 'Mexico',
        'code': 'MEX',
        'region': 'Latin America Caribbean',
        'population': 126190788,
        'land area': 1943950,
        'density': 65
    },
    {
        'name': 'United States',
        'code': 'USA',
        'region': 'North America',
        'population': 327167434,
        'land area': 9147420,
        'density': 36
    }
]

class Countries(Resource):
    
    def get(self):
    # get the data for a country with a matching country code

        # parse any arguments within the request
        parser = reqparse.RequestParser()
        parser.add_argument('code', action='append')
        parser.add_argument('region')
        parser.add_argument('sort_order')
        parser.add_argument('sort_by')
        parser.add_argument('limit')
        args = parser.parse_args()

        
        # filter and sort the data based on arguments
        data = countriesList

        if args['code']:
            data = [x for x in data if x['code'] in args['code']]
        
        if args['region']:
            data = [x for x in data if x['region'] == args['region']]
        
        if (args['sort_order'] == None or args['sort_order'].lower() == 'asc'):
            reverseOrder = False
        elif args['sort_order'].lower() == 'dsc':
            reverseOrder = True

        if args['sort_by']:
            data = sorted(data, key=lambda a: a[args['sort_by']], reverse=reverseOrder)
        
        if args['limit']:
            data = data[0:int(args['limit'])]
        
        # send the response in a JSON format
        if data:

            resource_fields = {}
            resource_fields['code'] = fields.String
            resource_fields['name'] = fields.String
            resource_fields['region'] = fields.String
            resource_fields['population'] = fields.Integer
            resource_fields['land area'] = fields.Integer
            resource_fields['density'] = fields.Integer
        
            data = {
                    'Status': 'Success',
                    'Error Code': 0,
                    'Message': 'Countries matching the criteria were found',
                    'Data': marshal(data, resource_fields)
            }     

            return data, 200

        else:

            data = {
                    'Status': 'Failed',
                    'Error Code': 1,
                    'Message': 'No countries were found matching criteria',
                    'Data': []
            }     

            return data, 404

    def post(self):
    # create a new country
    
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('code', type=str, required=True)
        parser.add_argument('region', type=str)
        parser.add_argument('population', type=int)
        parser.add_argument('landarea', type=int)
        parser.add_argument('density', type=int)
        args = parser.parse_args()

        for country in countriesList:
            if country['code'] == args['code']:
                return f"Error: Country with code {country['code']} already exists", 400

        new_country = {
            'name': args['name'],
            'code': args['code'],
            'region': args['region']
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


api.add_resource(Countries, '/api/countries', endpoint='countries')


if __name__ == '__main__':
    app.run(debug=True)