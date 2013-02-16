from flask.views import MethodView
from flask import request, jsonify, make_response, render_template
from flask.ext.login import login_required
from models import db
from utils.exceptions import abort

def to_json(datas):
    if type(datas)==list:
        return jsonify(items=datas)        
    return jsonify(datas)

encoders={'application/json':to_json,'text/html':render_template}

import hashlib
import uuid
import time

"""
Very importan encryption function that create a random salt with a timestamp
then concatenate this to the message to be hash and finally iterate it in order
to make it hard to rainbow the data.
"""
def encrypt_with_interaction(data,random_salt=str(uuid.uuid1()),iterate=50000,t = int(round(time.time()))):

    for i in range(0,iterate):
        data = hashlib.sha256(data+random_salt+str(t)).hexdigest()

    return data,iterate,t,random_salt

"""class KitchObject(object):
    def __init__(self, obj):        
        for k, v in obj.iteritems():
            if isinstance(v, dict):
                setattr(self, k, KitchObject(v))
            else:
                setattr(self, k, v)"""


class BaseService(MethodView):
    """
        Base class for services. Oriented to standarize the behaviour between the
        Resources.
    """
    schema_table=None

    @login_required
    def get(self,uid,template=None):
        """
        
        Get and validate offset and limit in query string.
        Handle expand parameter and return the list of expand entities.
        Template.

        """
        self.offset= int(self.get_parameter('offset'))
        self.limit= int(self.get_parameter('limit',50))
        self.expand=request.args.get('expand')
        self.template=template

        query = self.schema_table.query.filter_by(active=1)

        if uid :
            query.filter_by(uid=uid)
            model_object = query.first()
            return model_object

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

    def post_response(self):
        return make_response(to_json({'message':'Create succesfully'}),201,{'Location':request.url})

    def put_response(self):
        return make_response(to_json({'message':'Replace succesfully'}),200,{'Location':request.url})

    def delete_response(self):
        return make_response(to_json({ 'message':'Delete succesfully'}), 202)
        

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
            Post a single menu item and return 202 repsonse if successful
            {title:'TITLEMENU'}
        """

        json = request.json
        uid =str(uuid.uuid1())
        try:
            data_objects = self.object_from_json(uid,json)
        except KeyError as e:
            abort(400, 'Bad request Resource, please check the posted data %s' % e.message)

        for data_object in data_objects:
            db.session.add(data_object)

        db.session.commit()
        
        return self.post_response()

    @login_required
    def put(self):
        """
            PUT a single menu item and return 200 repsonse if successful
            {
                uid:'unique_identifier',
                title:'TITLEMENU'
            }
        """
        json=request.json
        self.update_object(json)
        db.session.commit()

        return self.put_response()

    @login_required
    def delete(self, uid):
        self.delete_entity(active=1, uid=uid)
        return self.delete_response()

    def delete_entity(self, **query_args):
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
        methods=['GET', 'DELETE'])


