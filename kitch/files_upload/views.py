import uuid
import os
from utils.entities import allowed_file
from flask import request, send_from_directory, current_app, url_for, redirect, Blueprint
from werkzeug import secure_filename

app = Blueprint('file_uploads',__name__,template_folder='templates')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],filename)

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(uuid.uuid1()) + '.' +  filename.rsplit('.',1)[1]
            
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('file_uploads.uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
#register_api(app,TableService, 'tableService','/table/','uid')