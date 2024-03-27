from flask import jsonify
from flask_restx import Resource, Namespace


service_info_ns = Namespace(name="service_info", description="Library object")


@service_info_ns.route("")
class ServiceInfo(Resource):

    def get(self):
        list_of_library = {
            "serviceInfo": {
                "position": [
                    {
                        "id": 1,
                        "value": "доцент",
                    },
                    {
                        "id": 2,
                        "value": "професор",
                    },
                ],
                "degree": [
                    {
                        "id": 1,
                        "value": "к.т.н",
                    },
                ],
                "university": [
                    {
                        "id": 1,
                        "name": "Харківський національний університет імені В.Н. Каразіна",
                        "universityAbbr": "ХНУ",
                        "cathedra": [
                            {
                                "id": 121,
                                "value": "Інженерія програмного забезпечення",
                            },
                        ],
                    },
                    {
                        "id": 2,
                        "name": "Харківський національний економічний університет імені Семена Кузнеця",
                        "universityAbbr": "ХНЕУ",
                        "cathedra": [
                            {
                                "id": 121,
                                "value": "Інженерія програмного забезпечення",
                            },
                        ],
                    },
                ],
                "specialty": [
                    {
                        "id": 1,
                        "specialtyNum": "121",
                        "specialtyName": "Інженерія програмного забезпечення",
                    },
                    {
                        "id": 2,
                        "specialtyNum": "122",
                        "specialtyName": "Комп'ютерні науки",
                    },
                ],
                "educationLevel": [
                    {
                        "id": 1,
                        "value": "бакалавр",
                    },
                    {
                        "id": 1,
                        "value": "магістр",
                    },
                ],
                "disciplineName": [
                    {
                        "id": 1,
                        "value": "test",
                    },
                ],
                "disciplineBlockName": [
                    {
                        "id": 1,
                        "value": "test",
                    },
                ],
                "disciplineGroupName": [
                    {
                        "id": 1,
                        "value": "test",
                    },
                ],
            },
        }
        return jsonify(list_of_library)
