from flask import Flask, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal
import json

app = Flask(__name__)
api = Api(app)

countriesList = [
    {
        'name': 'Argentina',
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
    
    def makeJSON(self, inputData, errorCode):

        print('Hello')
        
        if errorCode:
            status = 'Failed'
        else:
            status = 'Success'

        errorCodes = {
            0: '',
            1: 'No countries with matching criteria were found',
            2: 'Country with code already exists',
            3: 'Country with code could not be found'
        }

        resource_fields = {}
        resource_fields['code'] = fields.String
        resource_fields['name'] = fields.String
        resource_fields['region'] = fields.String
        resource_fields['population'] = fields.Integer
        resource_fields['land area'] = fields.Integer
        resource_fields['density'] = fields.Integer

        if inputData:
            jsonData = marshal(inputData, resource_fields)

        json_response = {
                'Status': status,
                'Error Code': errorCode,
                'Message': errorCodes[errorCode],
                'Data': jsonData
            }
        
        return json_response

    # def parseArguments(self, *args):
    #     parser = reqparse.RequestParser()
    #     if args:
    #         for a in args:
    #             parser.add_argument(a)
    #         return parser.parse_args()

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

            return make_response(
                   self.makeJSON(data, 0),
                   200)

        else:

            return make_response(
                   self.makeJSON(data, 1),
                   404)

    def post(self):
    # create a new country

        # parse any arguments within the request    
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('code', type=str, required=True)
        parser.add_argument('region', type=str)
        parser.add_argument('population', type=int)
        parser.add_argument('landarea', type=int)
        parser.add_argument('density', type=int)
        args = parser.parse_args()

        # check if the country already exists
        for country in countriesList:
            if country['code'] == args['code']:

                new_country = []

                return make_response(
                   self.makeJSON(new_country, 2),
                   400)

        # load a dictionary and insert into the database
        new_country = {
            'name': args['name'],
            'code': args['code'],
            'region': args['region'],
            'population': args['population'],
            'land area': args['landarea'],
            'density': args['density']
        }

        countriesList.append(new_country)

        return make_response(
                   self.makeJSON(new_country, 2),
                   200)

    def put(self):
    # update the data of an existing country with the matching country code

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('code', type=str)
        parser.add_argument('region', type=str)
        parser.add_argument('population', type=int)
        parser.add_argument('landarea', type=int)
        parser.add_argument('density', type=int)
        args = parser.parse_args()

        for country in countriesList:
            if country['code'] == args['code']:
                country['name'] = args['name']
                country['region'] = args['region']
                country['population'] = args['population']
                country['land area'] = args['landarea']
                country['density'] = args['density']
                updated_country = country

                return make_response(
                   self.makeJSON(updated_country, 0),
                   200)
        
        return make_response(
                   self.makeJSON(updated_country, 3),
                   400)


    def delete(self):

        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args()

        deletedCountry = []

        for country in countriesList:
            if country['code'] == args['code']:
                countriesList.remove(country)

                return make_response(
                   self.makeJSON(deletedCountry, 0),
                   200)
        
        return make_response(
                   self.makeJSON(deletedCountry, 3),
                   400)

api.add_resource(Countries, '/api/countries', endpoint='countries')


if __name__ == '__main__':
    app.run(debug=True)