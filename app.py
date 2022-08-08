#Package imports
from flask import Flask
from flask_restful import Resource, Api,reqparse

#local imports
from models import Project , db ,Samples

#Configs 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db'
api = Api(app)
db.init_app(app)
db.app = app
app.secret_key ='shivam'
UPLOAD_FOLDER = (r"C:\Users\shiva\OneDrive\Desktop\Hydrateq-backend\uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf','csv'])
#parse object for create project
create_project_parser = reqparse.RequestParser()
create_project_parser.add_argument("name")
create_project_parser.add_argument("aqurename")
#parse object for create project
create_sample_parser =  reqparse.RequestParser()
create_sample_parser.add_argument("name")
create_sample_parser.add_argument("place")
create_sample_parser.add_argument("ph")
create_sample_parser.add_argument("ph_4")
create_sample_parser.add_argument("tds")
create_sample_parser.add_argument("sodium")
create_sample_parser.add_argument("magnesium")
create_sample_parser.add_argument("calcium")
create_sample_parser.add_argument("sulfate")
create_sample_parser.add_argument("chloride")
create_sample_parser.add_argument("nitrate")
create_sample_parser.add_argument("carbonate")
create_sample_parser.add_argument("bicarbonate")
create_sample_parser.add_argument("iron")
create_sample_parser.add_argument("aluminium")
create_sample_parser.add_argument("Trioxidosilicate")
create_sample_parser.add_argument("Carbondioxide")

#show alll project ans create new project
class WaterData(Resource):
    def get(self):
        projects = Project.query.all()
        if len(projects) == 0:
            return {projects : 0},200
        else:
            project_info =[]
            for project in projects:
                project_info.append([project.id,project.name])
            return{
                "projects" : {"project":project_info }
            }
    def post(self):
        args = create_project_parser.parse_args()
        name = args.get("name")
        aqurename =args.get("aqurename")
        project= Project.query.filter_by(name= name).first()
        if project:
            return{
                "error code" : 1 ,
                "eror_message" :"Project  Name is already there"
            },400
        elif name == None :
            return{
                "error code": 1 ,
                "eror_message" :"Project  Name is required"
            }
        else:
            if aqurename == None:
                new = Project(name=name)
            else:
                new = Project(name= name ,aqurename=aqurename)
        db.session.add(new)
        db.session.commit()
        new = Project.query.filter_by(name=name).first()
        return {
            "id"  : new.id,
            "name" :new.name
        }

# show single project and create a new sample inside that project
class Projectsingle(Resource):
    def get(self ,id):
        project = Project.query.get(id)
        sample_info =[]
        for sample in project.samples :
            sample_info.append([sample.id,sample.name,sample.place])
        if project:
            return{
                "project_name" :project.name,
                "project_description" : project.aqurename,
                "project_samples" : {"samples":sample_info}
            },200
    def post(self,id):
        project = Project.query.get(id)
        if project:
            args = create_sample_parser.parse_args()
            name = args.get("name")
            place =args.get("place",None)
            project_id = id
            ph=args.get("ph")
            ph_4=args.get("ph_4")
            tds=args.get("tds")
            sodium=args.get("sodium")
            magnesium=args.get("magnesium")
            calcium=args.get("calcium")
            sulfate=args.get("sulfate")
            chloride=args.get("chloride")
            nitrate=args.get("nitrate")
            carbonate=args.get("carbonate")
            bicarbonate=args.get("bicarbonate")
            iron=args.get("iron")
            aluminium=args.get("aluminium")
            Trioxidosilicate=args.get("Trioxidosilicate")
            Carbondioxide=args.get("Carbondioxide")
            sample=Samples.query.filter_by(name=name , project_id=project_id).first()
            if sample:
                return{
                    "error code : 2 "
                    "eror_message" :"Sample  already there in current Project"
                },400
            elif name==None :
                return{
                    "error code ": 1,
                    "eror_message" :"Sample Name is required"
                }
            else:
                new = Samples(name=name,place=place,project_id = project_id,ph=ph,ph_4=ph_4,tds=tds,sodium=sodium,magnesium=magnesium,calcium=calcium,sulfate=sulfate,chloride=chloride,nitrate=nitrate,carbonate=carbonate,bicarbonate=bicarbonate,iron=iron,aluminium=aluminium,Trioxidosilicate=Trioxidosilicate,Carbondioxide=Carbondioxide)
            db.session.add(new)
            db.session.commit()
            new = Samples.query.filter_by(name = name).first()
            return {
                "id"  : new.id,
                "name" :new.name
            }  
        else:
            return{
                "error" : "no project avialble"
            } 


# show sigle project 
class Sample(Resource):
    def get(self,id):
        sample = Samples.query.get(id)
        if sample:
            return{
                "sample_name" :sample.name,
                "sample_description" : sample.place,
                "project_id" :sample.project_id,
                "ph" :sample.ph,
                "phat4degree": sample.ph_4,
                "tds" :sample.tds,
                "sodium" :sample.sodium,
                "magnesium" :sample.magnesium,
                "calcium " :sample.calcium ,
                "sulfate" :sample.sulfate,
                "chloride" :sample.chloride,
                "nitrate" :sample.nitrate,
                "carbonate" :sample.carbonate,
                "bicarbonate" :sample.bicarbonate,
                "iron" :sample.iron,
                "aluminium" :sample.aluminium,
                "Trioxidosilicate" :sample.Trioxidosilicate,
                "Carbondioxide":sample.Carbondioxide

            },200


#file upload 

#resources (end points)

api.add_resource(WaterData, '/')
api.add_resource(Projectsingle, '/project/<id>')
api.add_resource(Sample, '/sample/<id>')


# run app 
if __name__ == '__main__':
    app.run(debug=True)