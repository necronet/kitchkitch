from utils.entities import BaseService, register_api
from flask import Blueprint

class TableService(BaseService):
    def get(self, uid):
        query_result = super(TableService, self).get(uid)
        print query_result

app = Blueprint('table',__name__,template_folder='templates')
register_api(app,TableService, 'tableService','/table/','uid')