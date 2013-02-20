from utils.entities import BaseService, register_api
from models import Table
from flask import Blueprint

class TableService(BaseService):

    schema_table = Table

    def get(self, uid):
        query_result = super(TableService, self).get(uid)
        if type(query_result) == list:
            return self.get_response( [row.as_dict() for row in query_result] )
        else:
            return self.get_response(query_result.as_dict())


    def object_from_json(self, uid, json):
        return [Table(uid, json['name'])]

app = Blueprint('table',__name__,template_folder='templates')
register_api(app,TableService, 'tableService','/table/','uid')