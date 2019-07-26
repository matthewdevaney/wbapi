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
        
            outputJSON = {
                    'Status': 'Success',
                    'Error Code': 0,
                    'Message': 'Countries with matching criteria were found',
                    'Data': marshal(data, resource_fields)
            }     

            return make_response(outputJSON, 200)

        else:

            outputJSON = {
                    'Status': 'Failed',
                    'Error Code': 1,
                    'Message': 'No countries with matching criteria were found',
                    'Data': []
            }     

            return make_response(outputJSON, 404)

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

                outputJSON = {
                        'Status': 'Failed',
                        'Error Code': 2,
                        'Message': f"Country with code {country['code']} already exists",
                        'Data': []
                }

                return make_response(outputJSON, 400)

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

        # send the response in a JSON format
        resource_fields = {}
        resource_fields['code'] = fields.String
        resource_fields['name'] = fields.String
        resource_fields['region'] = fields.String
        resource_fields['population'] = fields.Integer
        resource_fields['land area'] = fields.Integer
        resource_fields['density'] = fields.Integer

        outputJSON = {
                'Status': 'Success',
                'Error Code': 0,
                'Message': f"Country with code {country['code']} was added",
                'Data': marshal(new_country, resource_fields)
        }

        return make_response(outputJSON, 200)

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

                resource_fields = {}
                resource_fields['code'] = fields.String
                resource_fields['name'] = fields.String
                resource_fields['region'] = fields.String
                resource_fields['population'] = fields.Integer
                resource_fields['land area'] = fields.Integer
                resource_fields['density'] = fields.Integer

                outputJSON = {
                            'Status': 'Success',
                            'Error Code': 0,
                            'Message': f"Country with code {country['code']} was updated",
                            'Data': marshal(country, resource_fields)
                }

                return make_response(outputJSON, 200)
        
        outputJSON = {
                    'Status': 'Failed',
                    'Error Code': 3,
                    'Message': f"Country with code {args['code']} could not be found",
                    'Data': []
        }     

        return make_response(outputJSON, 400)


    def delete(self):

        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args()

        for country in countriesList:
            if country['code'] == args['code']:
                countriesList.remove(country)

                outputJSON = {
                    'Status': 'Success',
                    'Error Code': 0,
                    'Message': f"Success: Country with code {country['code']} was removed",
                    'Data': []
                }

                return make_response(outputJSON, 200)
        
        outputJSON = {
                    'Status': 'Success',
                    'Error Code': 3,
                    'Message': f"Country with code {args['code']} could not be found",
                    'Data': []
        }

        return (outputJSON, 400)


api.add_resource(Countries, '/api/countries', endpoint='countries')


if __name__ == '__main__':
    app.run(debug=True)