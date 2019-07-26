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
   
    # parse any arguments passed with the request
    def parseArguments(self, *args):
        parser = reqparse.RequestParser()

        integerArguments = ['population', 'landarea', 'density']
        stringArguments = ['code','name','region','population','sort_by','sort_order','limit']

        for a in args:
            if a in integerArguments:
                parser.add_argument(a, type=int)
            else:
                parser.add_argument(a, type=str)
        return parser.parse_args()

    # make a dictionary object representing a country
    def constructCountry(self, data):
        return {
            'name': data['name'],
            'code': data['code'],
            'region': data['region'],
            'population': data['population'],
            'land area': data['landarea'],
            'density': data['density']
        }

    # construct the JSON returned with the response
    def makeJSON(self, inputData, errorCode):
        
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
        else:
            jsonData = []

        json_response = {
                'Status': status,
                'Error Code': errorCode,
                'Message': errorCodes[errorCode],
                'Data': jsonData
            }
        
        return json_response
        
    def get(self):
    # get the data for a country with a matching country code

        # parse any arguments within the request
        args = self.parseArguments('code','region','sort_order','sort_by','limit')

        # filter and sort the data based on arguments
        data = countriesList

        if args['code']:
            data = [x for x in data if x['code'] == args['code']]
        
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
        args = self.parseArguments('name','code','region','population','landarea','density')

        # check if the country already exists
        for country in countriesList:
            if country['code'] == args['code']:

                new_country = []

                return make_response(
                   self.makeJSON(new_country, 2),
                   400)

        # load a dictionary and insert into the database
        new_country = constructCountry(args)

        countriesList.append(new_country)

        return make_response(
                   self.makeJSON(new_country, 2),
                   200)

    def put(self):
    # update the data of an existing country with the matching country code

        args = self.parseArguments('name','code','region','population','landarea','density')

        for country in countriesList:
            if country['code'] == args['code']:
                updated_country = constructCountry(args)

                return make_response(
                   self.makeJSON(updated_country, 0),
                   200)
        
        return make_response(
                   self.makeJSON(updated_country, 3),
                   400)


    def delete(self):

        args = self.parseArguments('code')

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