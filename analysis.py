from math import sqrt
from models import *

def analyze(id):
        datas=Samples.query.all()
        sum=38
        indicator=["pH","Tds","ca","mg","na","k","hco3","so4","cl","no3","f"]
        Wi=[2/sum,4/sum,3/sum,5/sum,4/sum,2/sum,1/sum,3/sum,4/sum,5/sum,5/sum]
        whostandards=[7,1000,300,30,200,12,500,250,250,50,1.5]
        cgwbstandard=[range(6.5-8.6),range(500,2001),range(75,101),range(30,100),range(200-400),range(250-1000),45,range(1.0-1.5)]#no range for sodium and potassium,hco3
        x=0
        wqivalue=0
        for data in datas:
                ph=data.pH
                tds=data.TDS
                no3=data.NO3
                f=data.F
                na=data.Na
                ca=data.Ca
                mg=data.Mg
                k=data.k
                hco3=data.HCO3
                co3=data.CO3
                cl=data.Cl
                so4=data.SO4

                sar=na/sqrt(mg+ca)
                solNa=(na/(ca+mg+na+k))*100
                rsc=(hco3+co3)-(ca+mg)
                wqivalue+=(Wi[x]*ph*100)/whostandards[x]
                x+=1
                img = Analysis(id=id,sar=sar,solNa=solNa, rsc=rsc,wqi=wqivalue)
                db.session.add(img)
                db.session.commit()




