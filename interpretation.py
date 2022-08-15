from models import Samples
import analysis
result=""
minphdes=""
maxphdes=""
def pHCal(min,max,mean):

    minphdes=__phval(min)
    maxphdes=__phval(max)
    result=f"The pH of Groundwater of given area ranges from {minphdes} ({min}) to {maxphdes}({max}) with pH {mean} as mean"
    print(result)

def __phval(ph):#whether it is highly or slightly alkaline acidic neutral


    value=""
    if ph <7.0:
        if ph <5.5:
            value="Highly Acidic"
        else:
            value="Slightly Acidic"
    elif ph > 7.0:
        if ph >8.5:
            value="Highly Alkaline"
        else:
            value+="Slightly Alkaline"
    else :
        value="Neutral"
    return value   





