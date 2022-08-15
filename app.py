# Package imports
import glob
from typing import final
from flask import Flask, Response
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os
import werkzeug
import pandas as pd
import json
import base64
from wqchartpy import gibbs, triangle_piper, rectangle_piper, color_piper, durvo, hfed, chadha, schoeller
# local imports
from models import Project, db, Samples, CsvLog, Result
from dataclean import clustering, cleandata
from Graphs.triangle_piper import piper
# Configs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db'
api = Api(app)
CORS(app)
db.init_app(app)
db.app = app
app.secret_key = 'shivam'
basedir = os.path.abspath(os.path.dirname(__file__))
uploads_path = os.path.join(basedir, 'uploads')
current_path = os.getcwd()


# UPLOAD_FOLDER = ('static/uploads')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# parse object for create project


create_project_parser = reqparse.RequestParser()
create_project_parser.add_argument("name")
create_project_parser.add_argument("aqurename")

# parse object for create project

create_sample_parser = reqparse.RequestParser()
create_sample_parser.add_argument("name")
create_sample_parser.add_argument("x")
create_sample_parser.add_argument("y")
create_sample_parser.add_argument("long")
create_sample_parser.add_argument("lat")
create_sample_parser.add_argument("alk")
create_sample_parser.add_argument("ph")
create_sample_parser.add_argument("ph_4")
create_sample_parser.add_argument("tds")
create_sample_parser.add_argument("hardness")
create_sample_parser.add_argument("sodium")
create_sample_parser.add_argument("potassiumSodium")
create_sample_parser.add_argument("magnesium")
create_sample_parser.add_argument("calcium")
create_sample_parser.add_argument("sulfate")
create_sample_parser.add_argument("chloride")
create_sample_parser.add_argument("fluoride")
create_sample_parser.add_argument("nitrate")
create_sample_parser.add_argument("carbonate")
create_sample_parser.add_argument("bicarbonate")
create_sample_parser.add_argument("iron")
create_sample_parser.add_argument("aluminium")
create_sample_parser.add_argument("Trioxidosilicate")
create_sample_parser.add_argument("Carbondioxide")
csv_parser = reqparse.RequestParser()
csv_parser.add_argument(
    "file", type=werkzeug.datastructures.FileStorage, location='files')

# show alll project and create new project


class WaterData(Resource):
    def get(self):
        projects = Project.query.all()
        if len(projects) == 0:
            return {"projects": 0}, 200
        else:
            project_info = []
            for project in projects:
                project_info.append(
                    (project.id, project.name, project.aqurename))
            return {
                "projects": project_info
            }

    def post(self):
        args = create_project_parser.parse_args()
        name = args.get("name")
        aqurename = args.get("aqurename")
        project = Project.query.filter_by(name=name).first()
        if project:
            return {
                "error code": 1,
                "eror_message": "Project  Name is already there"
            }, 400
        elif name == None:
            return {
                "error code": 1,
                "eror_message": "Project  Name is required"
            }
        else:
            if aqurename == None:
                new = Project(name=name)
            else:
                new = Project(name=name, aqurename=aqurename)
        db.session.add(new)
        db.session.commit()
        new = Project.query.filter_by(name=name).first()
        return {
            "id": new.id,
            "name": new.name
        }

# show single project and create a new sample inside that project


class Projectsingle(Resource):
    def get(self, id):
        project = Project.query.get(id)
        sample_info = []
        for sample in project.samples:
            sample_info.append([sample.id, sample.name, sample.place])
        if project:
            return {
                "project_name": project.name,
                "project_description": project.aqurename,
                "project_samples": {"samples": sample_info}
            }, 200

    def post(self, id):
        project = True
        if project:
            args = create_sample_parser.parse_args()
            name = args.get("name")
            place = args.get("place", None)
            project_id = id
            x = args.get("x")
            y = args.get("y")
            long = args.get("long")
            lat = args.get("lat")
            alk = args.get("alk")
            hardness = args.get("hardness")
            ph = args.get("ph")
            ph_4 = args.get("ph_4")
            tds = args.get("tds")
            sodium = args.get("sodium")
            potassiumSodium = args.get("potassiumSodium")
            magnesium = args.get("magnesium")
            calcium = args.get("calcium")
            sulfate = args.get("sulfate")
            chloride = args.get("chloride")
            fluoride = args.get("fluoride")
            nitrate = args.get("nitrate")
            carbonate = args.get("carbonate")
            bicarbonate = args.get("bicarbonate")
            iron = args.get("iron")
            aluminium = args.get("aluminium")
            Trioxidosilicate = args.get("Trioxidosilicate")
            Carbondioxide = args.get("Carbondioxide")
            sample = Samples.query.filter_by(
                name=name, project_id=project_id).first()
            if sample:
                return {
                    "error code : 2 "
                    "eror_message": "Sample  already there in current Project"
                }, 400
            elif name == None:
                return {
                    "error code ": 1,
                    "eror_message": "Sample Name is required"
                }
            else:
                new = Samples(name=name, x=x, y=y, long=long, lat=lat, project_id=project_id, ph=ph, ph_4=ph_4, alk=alk, hardness=hardness, tds=tds, sodium=sodium, potassiumSodium=potassiumSodium, magnesium=magnesium, calcium=calcium,
                              sulfate=sulfate, chloride=chloride, fluoride=fluoride, nitrate=nitrate, carbonate=carbonate, bicarbonate=bicarbonate, iron=iron, aluminium=aluminium, Trioxidosilicate=Trioxidosilicate, Carbondioxide=Carbondioxide)
            db.session.add(new)
            db.session.commit()
            new = Samples.query.filter_by(name=name).first()
            return {
                "id": new.id,
                "name": new.name
            }
        else:
            return {
                "error": "no project avialble"
            }


# show sigle project
class Sample(Resource):
    def get(self, id):
        samples = Samples.query.filter_by(project_id= id).all()
        for sample in samples:
            return {
                "sample_name": sample.name,
                "sample_description": sample.place,
                "project_id": sample.project_id,
                "ph": sample.ph,
                "x": sample.x,
                "y": sample.y,
                "long": sample.long,
                "lat": sample.lat,
                "phat4degree": sample.ph_4,
                "alk": sample.alk,
                "hardness": sample.hardness,
                "tds": sample.tds,
                "tds": sample.tds,
                "sodium": sample.sodium,
                "potassiumSodium": sample.potassiumSodium,
                "magnesium": sample.magnesium,
                "calcium ": sample.calcium,
                "sulfate": sample.sulfate,
                "chloride": sample.chloride,
                "fluoride": sample.fluoride,
                "nitrate": sample.nitrate,
                "carbonate": sample.carbonate,
                "bicarbonate": sample.bicarbonate,
                "iron": sample.iron,
                "aluminium": sample.aluminium,
                "Trioxidosilicate": sample.Trioxidosilicate,
                "Carbondioxide": sample.Carbondioxide
            }, 200
class csv_upload(Resource):
    def get(self, id):
        place = CsvLog.query.filter_by(project_id=id).first()
        if (place):
            try:
                df = pd.read_csv("file"+str(id)+".csv")
                res = df.to_json()
                return json.loads(res), 200
            except FileNotFoundError:
                return "Upload your data", 201

    def post(self, id):
        args = csv_parser.parse_args()
        file = args.get("file")
        try:
           # delete all graph with this id from data databse +file 
            os.remove("file"+str(id)+".csv")
        finally:  
            if file:
                file.save(os.path.join(uploads_path, id+file.filename))
                location = os.path.join(uploads_path, id+file.filename)
                csv = CsvLog(location=location, project_id=id)
                db.session.add(csv)
                db.session.commit()
                raw_df = pd.read_csv(location)
                data = cleandata(raw_df)[0]
                res = data.to_json(orient='index')
                readydata = clustering(raw_df)
                piper(readydata, unit='mg/L',
                    figname='trianglePiperdiagram'+id, figformat='jpg')
                img = open('trianglePiperdiagram'+id+'.jpg', 'rb').read()
                new_graph = Result(project_id=id, image=img,
                                name='trianglePiperdiagram')
                db.session.add(new_graph)
                db.session.commit()

                gibbs.plot(readydata, unit='mg/L',
                        figname='gibbsDiagram'+id, figformat='jpg')
                img = open('gibbsDiagram'+id+'.jpg', 'rb').read()
                new_graph = Result(project_id=id, image=img, name='gibbsDiagram')
                db.session.add(new_graph)
                db.session.commit()

                rectangle_piper.plot(readydata, unit='mg/L', figname='rectanglePiper'+id, figformat='jpg')
                img= open('rectanglePiper'+id+'.jpg','rb').read()
                new_graph = Result(project_id=id,image=img ,name='rectanglePiper')
                db.session.add(new_graph)
                db.session.commit()

                durvo.plot(readydata, unit='mg/L', figname='durvoDiagram'+id, figformat='jpg')
                img= open('durvoDiagram'+id+'.jpg','rb').read()
                new_graph = Result(project_id=id,image=img ,name='durvoDiagram')
                db.session.add(new_graph)
                db.session.commit()

                hfed.plot(readydata, unit='mg/L', figname='hfedDiagram'+id, figformat='jpg')
                img= open('hfedDiagram'+id+'.jpg','rb').read()
                new_graph = Result(project_id=id,image=img ,name='hfedDiagram')
                db.session.add(new_graph)
                db.session.commit()

                chadha.plot(readydata, unit='mg/L', figname='chadhaDiagram'+id, figformat='jpg')
                img= open('chadhaDiagram'+id+'.jpg','rb').read()
                new_graph = Result(project_id=id,image=img ,name='chadhaDiagram')
                db.session.add(new_graph)
                db.session.commit()

                color_piper.plot(readydata, unit='mg/L', figname='color_piperDiagram'+id, figformat='jpg')
                img= open('color_piperDiagram'+id+'.jpg','rb').read()
                new_graph = Result(project_id=id,image=img ,name='color_piperDiagram')
                db.session.add(new_graph)
                db.session.commit()

                schoeller.plot(readydata, unit='mg/L', figname='schoellerDiagram'+id, figformat='jpg')
                img= open('schoellerDiagram'+id+'.jpg','rb').read()
                new_graph = Result(project_id=id,image=img ,name='schoellerDiagram')
                db.session.add(new_graph)
                db.session.commit()
                data.to_csv('file'+str(id)+'.csv')
                return "succes"
            else:
                return {
                    "message": "no files uploaded"
                }


    # def get(self,id):
    #     graph = Result.query.filter_by(project_id=id,name="trianglePiperdiagram").first()
    #     if graph:
    #         return Response(graph.image, mimetype=graph.mimetype)


@app.route('/graph/<name>/<int:id>')
def get_img(id, name):
    # global imag_file
    img = Result.query.filter_by(project_id=id, name=name).first()
    if not img:
        return 'Invalid data to generate graph', 404
    # imag_file=f"http://127.0.0.1:5000/2"
    return Response(img.image, mimetype=img.name)


api.add_resource(WaterData, '/')
api.add_resource(Projectsingle, '/project/<id>')
api.add_resource(Sample, '/sample/<id>')
api.add_resource(csv_upload, '/csv/<id>')
# run app
if __name__ == '__main__':
    app.run(debug=True)



