from flask_restx import Resource, Namespace

city = Namespace(name="cities", description="Cities of Ukraine")


@city.route("")
class Hello(Resource):
    def get(self):
        return {"Hello": "city"}
