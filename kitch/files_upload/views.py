import uuid
import os
from utils.entities import allowed_file
from flask import request, send_from_directory, current_app, url_for, redirect, Blueprint
from flask.views import MethodView
from werkzeug import secure_filename

app = Blueprint('file_uploads',__name__,template_folder='templates')

class FileUpload(MethodView):

    def get(self, uid):
        return send_from_directory(current_app.config['UPLOAD_FOLDER'],uid)

    def post(self):
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uid = str(uuid.uuid1())
            filename = uid + '.' +  filename.rsplit('.',1)[1]
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('file_uploads.uploaded_file',uid=uid))