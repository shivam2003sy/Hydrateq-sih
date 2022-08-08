#imports
from flask_sqlalchemy import SQLAlchemy
#configs
db = SQLAlchemy()


#project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    aqurename = db.Column(db.String)
    samples = db.relationship('Samples', backref='project', lazy=True)
    def __repr__(self):
        return '<Projectname %r>' % self.name

#Sample models
class Samples(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    place = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'),nullable=False)
    ph=db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    ph_4=db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    tds =db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    sodium = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    magnesium = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    calcium = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    sulfate = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    chloride = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    nitrate = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    carbonate = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    bicarbonate = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    iron = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    aluminium = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    Trioxidosilicate = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    Carbondioxide =db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    def __repr__(self):
        return '<Sample%r>' % self.name