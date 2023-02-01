from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    
    fullname = db.Column(db.String(80), unique=False, nullable=False)
    address1 = db.Column(db.String(80), unique=False, nullable=False)
    address2 = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    state = db.Column(db.String(80), unique=False, nullable=False)
    npostal = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password":self.password,
            "fullname":self.fullname,
            "address1":self.address1,
            "address2":self.address2,
            "city": self.city,
            "state":self.state,
            "npostal":self.npostal
            # do not serialize the password, its a security breach
        }

class Diccionario(db.Model):
    __tablename__="diccionario"
    id = db.Column(db.Integer, primary_key=True)
    tipo_situacion = db.Column(db.String(120), unique=True, nullable=False)
    url_img = db.Column(db.String(120), unique=True, nullable=False)
    url_video = db.Column(db.String(120), unique=True, nullable=False)
    tipo_url = db.Column(db.String(120), unique=True, nullable=False)
    

    def __repr__(self):
        return '<Diccionario %r>' % self.tipo_situacion

    def serialize(self):
        return {
            "id": self.id,
            "tipo_situacion": self.tipo_situacion,
            "url_img": self.url_img,
            "url_video": self.url_video
            # do not serialize the password, its a security breach
        }

class Me_gusta(db.Model):
    __tablename__="me_gusta"
    id = db.Column(db.Integer, primary_key=True)
    id_diccionario = db.Column(db.Integer, db.ForeignKey('diccionario.id'), nullable=False)
    tipo_situacion = db.relationship('Diccionario')
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tipo_user = db.relationship('User')
    
    def __repr__(self):
        return '<Me_gusta %r>' % self.id_diccionario

    def serialize(self):
        return {
            "id": self.id,
            "diccionario": self.diccionario,
            # do not serialize the password, its a security breach
        }

