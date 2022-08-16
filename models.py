#imports
from ast import NamedExpr
from email.mime import image
from unicodedata import name
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.dialects.oracle import BLOB
#configs
db = SQLAlchemy()

#project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    aqurename = db.Column(db.String)
    samples = db.relationship('Samples', backref='project', lazy=True)
    csvLog = db.relationship('CsvLog', backref='project', lazy=True)
    result = db.relationship('Result', backref='project', lazy=True)
    def __repr__(self):
        return '<Projectname %r>' % self.name
#Sample models
class Samples(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    x=db.Column(db.Integer)
    y=db.Column(db.Integer)
    long=db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    lat=db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'),nullable=False)
    ph=db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    ph_4=db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    alk=db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    hardness=db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    tds =db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    sodium = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    potassiumSodium=db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    magnesium = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    calcium = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    sulfate = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    chloride = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    fluoride = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    nitrate = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    carbonate = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    bicarbonate = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    iron = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    aluminium = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    Trioxidosilicate = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    Carbondioxide =db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    def __repr__(self):
        return '<Sample%r>' % self.name
#class for the result model
class CsvLog(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'),nullable=False)
    location = db.Column(db.String , nullable=False)
    def __repr__(self):
        return '<CsvLog%r>' % self.project_id


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'),nullable=False)
    image = db.Column(BLOB, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Result%r>' % self.name


#Analysis
class Analysis(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'),nullable=False)
    sar=db.Column(db.Float)
    solNa=db.Column(db.Float)
    rsc=db.Column(db.Float)
    wqi=db.Column(db.Float)