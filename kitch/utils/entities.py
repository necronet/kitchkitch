from flask.views import MethodView
from flask import request,  make_response, render_template, json
from flask.ext.login import login_required
from models import db
from utils.exceptions import abort
import sqlalchemy
import hashlib
import uuid
import decimal
import time

class APIEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, decimal.Decimal):
            return str(obj)

        return json.JSONEncoder.default(self, obj)

def to_json(datas):
    if type(datas)==list:
        return jsonify(items=datas)
    return jsonify(datas)

#List of available encoding function to be returned.
encoders={'application/json':to_json,'text/html':render_template}

def encrypt_with_interaction(data,random_salt=str(uuid.uuid1()),iterate=50000,t = int(round(time.time()))):
    """
    Very importan encryption function that create a random salt with a timestamp
    then concatenate this to the message to be hash and finally iterate it in order
    to make it hard to rainbow the data.
    """

    for i in range(0,iterate):
        data = hashlib.sha256(data+random_salt+str(t)).hexdigest()

    return data,iterate,t,random_salt

def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['jpg', 'png']
    """
        check wether a filename is acceptable
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class BaseService(MethodView):
    """
        Base class for services. Oriented to standarize the behaviour between the
        Resources.
    """
    schema_table=None

    @login_required
    def get(self, uid=None, template=None, join= None, *join_criterion,**kwargs):
        """
        Base method for retrieving objects from a resource it will by default:

        - Validate offset and limit as wel as other query string parameters.
        - Query from the schema_table a list or a single record (if uid was provided).
        - In case no record can be found a 404 will be thrown.

        """
        self.offset= int(self.get_parameter('offset'))
        self.limit= int(self.get_parameter('limit',50))
        self.expand=request.args.get('expand')
        self.template=template

        query = self.schema_table.query.filter_by(active=1)

        if uid:
            query = query.filter_by(uid=uid)
            model_object = query.first()

            return model_object if model_object else abort(404, "Resources was not found")

        if join:
            query = query.join(join)

        if len(kwargs)>0:
            query = query.filter_by(**kwargs)


        query.limit(self.limit).offset(self.offset)

        return query.all()

    def get_parameter(self, param_name, default_value=0):
        parameter=request.args.get(param_name)
        return default_value if parameter is None or type(parameter)!=type(default_value) else parameter

    def get_response(self, datas):
        #Will get the best match between supported mimes see encoder_types dictionary
        encoder_key=request.accept_mimetypes.best_match(encoders.keys())
        
        #This is very clever way to mutate, will dinamically return  a function and will pass the proper data
        return encoders[encoder_key](datas)

    def post_response(self, json_response, uid):
        return make_response(json_response,201,{'Location':request.url+uid})

    def put_response(self):
        return make_response(to_json({'message':'Replace succesfully'}),200,{'Location':request.url})

    def delete_response(self):
        return make_response(to_json({ 'message':'Delete succesfully'}), 204)
        

    def expand_arguments(self):
        """
        Will check the expand attribute is present and try to get the attributes
        from the expand parameter. i.e

        The following expression:

            http://foo/?expand=item,user

        Should return a list: [item,user]

        """
        if self.expand is None:
            return []

        expand_arguments=[]
        for attribute in self.expand.split(','):
            expand_arguments.append(attribute)

        return expand_arguments

    @login_required
    def post(self):
        """
            Post a single menu item and return 204 repsonse if successful
            {title:'TITLEMENU'}
        """

        json = request.json
        uid =str(uuid.uuid1())
        try:
            data_objects = getattr(self, "object_from_json")(uid,json)
        except AttributeError as e:
            abort(501, 'Method not implemented %s' % e.message)
        except KeyError as e:
            abort(400, 'Bad request Resource, please check the posted data %s' % e.message)

        try:
            for data_object in data_objects:
                db.session.add(data_object)

            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            abort(409, 'Conflict on creating record. %s' % e.message)
        
        response_object = self.get(uid);
        

        return self.post_response(response_object.data, uid)

    @login_required
    def put(self, uid=None):
        """
            PUT a single menu item and return 200 repsonse if successful
            {
                uid:'unique_identifier',
                title:'TITLEMENU'
            }
        """
        json=request.json
        try:
            getattr(self,"update_object")(json)
        except AttributeError as e:
            abort(501, "Method not implemented %s" % e.message)
        db.session.commit()

        return self.put_response()

    @login_required
    def delete(self, uid):
        self.delete_entity(active=1, uid=uid)
        return self.delete_response()

    def delete_entity(self, schema_table=None, **query_args):
        if schema_table:
            self.schema_table = schema_table
        
        model=self.schema_table.query.filter_by(**query_args).first()
        model.active=0
        db.session.commit()


def register_api(app,view, endpoint, url, pk, pk_type='string'):
    """
    Register a MethodView class to hold the standard pattern

    GET: /url/
    GET, DELETE: /url/[id]
    PUT,POST: /url
    """
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
        view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST','PUT',])
    app.add_url_rule('%s<%s:%s>' %(url,pk_type,pk), view_func=view_func,
        methods=['GET', 'DELETE','PUT'])


from itsdangerous import simplejson as _json
from flask import current_app

def jsonify(*args, **kwargs):
    """
    Rewrite jsonify to force use of API_ENcoder unil 0.10 is release 
    """
    return current_app.response_class(dumps(dict(*args, **kwargs),
        indent=None if request.is_xhr else 2),
        mimetype='application/json')

def dumps(obj, **kwargs):   
    _dump_arg_defaults(kwargs)
    return _json.dumps(obj, **kwargs)

def _dump_arg_defaults(kwargs):
    """Inject default arguments for dump functions."""
    if current_app:
        kwargs.setdefault('cls', current_app.json_encoder)
        if current_app.config.has_key('JSON_AS_ASCII') and not current_app.config['JSON_AS_ASCII']:
            kwargs.setdefault('ensure_ascii', False)

