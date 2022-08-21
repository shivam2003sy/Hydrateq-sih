from math import sqrt
from threading import local
from models import *
import pandas as pd
from dataclean import clustering
import csv
def feed(id,location):
    # raw_df = pd.read_csv("uploads/1sample.csv")
    # readydata = clustering(raw_df)

    with open(location, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                try:
                    for row in csv_reader:
                        name = "sample"+str(line_count)
                        project_id = id
                        x=row["X"]
                        y=row["Y"]
                        long=row["Longitude"]
                        lat=row["Latitude"]
                        ph=row["pH"]
                        alk=row["Alk"]
                        hardness=row["Hardness"]
                        tds=row["TDS"]
                        calcium=row["Ca"]
                        magnesium=row["Mg"]
                        sodium = row["Na"]
                        potassiumSodium=row["KNa"]
                        calcium=row["Cl"]
                        sulfate=row["SO4"]
                        bicarbonate =row["HCO3"]
                        nitrate=row["NO3"]
                        iron=row["F"]
                        sample = Samples(name=name,x=x, y=y , long=long, lat=lat ,project_id=project_id, ph=ph, alk=alk, hardness=hardness, tds=tds, magnesium=magnesium, sodium=sodium, potassiumSodium=potassiumSodium, calcium=calcium, sulfate=sulfate, bicarbonate=bicarbonate, nitrate=nitrate, iron=iron)
                        db.session.add(sample)
                        db.session.commit()
                        line_count += 1
                        if line_count == 2:
                            break
                finally:
                    csv_file.close()
    return "uploaded"
def analyze(id):
        datas=Samples.query.filter_by(project_id=id).all()
        sum=38
        indicator=["pH","Tds","ca","mg","na","k","hco3","so4","cl","no3","f"]
        Wi=[2/sum,4/sum,3/sum,5/sum,4/sum,2/sum,1/sum,3/sum,4/sum,5/sum,5/sum]
        whostandards=[7,1000,300,30,200,12,500,250,250,50,1.5]
        # cgwbstandard=[range(6.5-8.6),range(500,2001),range(75,101),range(30,100),range(200-400),range(250-1000),45,range(1.0-1.5)]#no range for sodium and potassium,hco3
        x=0
        wqivalue=0
        for data in datas:
                ph=data.ph
                tds=data.tds
                no3=data.nitrate
                f=data.iron
                na=data.sodium
                ca=data.calcium
                mg=data.magnesium
                k=data.potassiumSodium
                hco3=data.bicarbonate
                co3=data.carbonate
                cl=data.chloride
                so4=data.sulfate

                if hco3==None:
                    hco3=0
                if co3==None:
                    co3=0
                if cl==None:
                    cl=0
                if so4==None:
                    so4=0
                if na==None:
                    na=0
                if ca==None:
                    ca=0    
                if mg==None:
                    mg=0
                if k==None:                    
                    k=0
                sar=na/sqrt(mg+ca)
                solNa=(na/(ca+mg+na+k))*100
                rsc=(hco3+co3)-(ca+mg)
                wqivalue+=(Wi[x]*ph*100)/whostandards[x]
                x+=1
                img = Analysis(project_id=id,sar=sar,solNa=solNa, rsc=rsc,wqi=wqivalue )
                db.session.add(img)
                db.session.commit()
        return "analyzed"