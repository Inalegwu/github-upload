 from student_portal import app

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
