from flask import Flask ,flash,redirect,render_template,url_for,request
import os
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from ColorDector import ColorDetector


UPLOAD_FOLDER = '/static/res' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
file = FileStorage()

app  = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY']  = '@#2hru4$%45'

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response
"tempo.png"
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/',methods = ['POST','GET'])
def home():
    global file
    if request.method=='POST':
        file = request.files['File']
        if 'File' not in request.files:
            return render_template('filenotfound.html')
        
        if file.filename == '':
            flash("No Image is Selected","Error")
            return(render_template('index.html'))
             
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Your Image is in the Window  , Check Your On Going App And Click the area for which you want image color",'Success')
            return(redirect(url_for('filerecieved')))
        else:
            flash("Error",'error')
            return render_template('filenotfound.html')
            
    else:
        return(render_template('index.html'))
    
@app.route("/file_submitted")
def filerecieved():
    return(render_template('filerecieve.html'))

@app.route("/selectimg",methods=['POST'])
def selectimg():
    global file
    filename =  secure_filename(file.filename)
    fileNameIs = UPLOAD_FOLDER+'/'+filename
    return(render_template("selectimage.html",Image = fileNameIs ))


@app.route('/startprocessing',methods = ['POST'])
def processing():
    global file
    if request.method =='POST':
        filename =  secure_filename(file.filename)
        xPoint = int (request.form['xval'])
        yPoint = int(request.form['yval'])
        
        ans,r,g,b= ColorDetector(UPLOAD_FOLDER+'/'+filename,xPoint,yPoint,2)
        if os.path.isfile(UPLOAD_FOLDER+'/'+filename):
            os.remove(UPLOAD_FOLDER+'/'+filename)
        file = None
        return (redirect(url_for('subme',Color_name =ans,red = r,green = g,blue = b )))
    

@app.route("/Submit<Color_name>/<red>/<green>/<blue>")
def subme(Color_name,red,green,blue):
    return (render_template('Colorres.html',Color = Color_name , red =red,green = green,blue = blue ) )
        
            

if __name__ == '__main__':
    app.run()
