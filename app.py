from flask import Flask,redirect,render_template,flash,request,url_for,Response
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
from flask_login import LoginManager,login_user,UserMixin,current_user,login_required,logout_user
from werkzeug.security import check_password_hash,generate_password_hash
from flask_admin import Admin
from camera import Camera
from time import time

app=Flask(__name__)
app.config['SECRET_KEY']='njdcsj35445jmdflkfdfvdscd'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///modelDatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
bcrypt=Bcrypt(app)
db=SQLAlchemy(app)
login_manager=LoginManager(app)
admin=Admin(app,'Blog Admin')

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))

class Student(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False)
    password_hash=db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password Is Not Readable')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return 'Student'+str(self.username)


class Camera(object):
    def __init__(self):
        self.frames=[open(f+'.jpg','rb').read()for f in ['1','2','3']]

    def get_frame(self):
        return self.frames[int(time())%3]


@app.route('/',methods=['GET','POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        stud=Student.query.filter_by(username=form.username.data).first()
        if stud is not None and stud.verify_password(form.password.data):
            login_user(stud)
            flash('Logged In Successfully. Welcome  '+str(form.username.data)+" !",'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed,Check Your Username And Password','danger')
    return render_template('index.html',form=form,title="Login")

@app.route('/home')
@login_required
def home():
    return render_template('home.html',title="Dashboard")
@app.route('/logout')
def logout():
    logout_user()
    flash('Logged Out Login To Continue Communicating',"info")
    return  redirect(url_for('index',title="Login"))


@app.route('/classroom')
def classroom():
    return render_template('class.html',title="Class")

@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html',title="Unauthorized")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',title="Page Not Found")


def gen(camera):
    frame=camera.get_frame()
    yield (b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+frame+b'\r\n')
@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),mimetype='multipart/x-mixed-replace:boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)