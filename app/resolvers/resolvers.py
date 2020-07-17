from __future__ import division
# imports
import math
import json
from scipy.signal import butter, lfilter
import numpy as np
import pandas as pd
# helpers

def getResultant(accel):
    x = math.pow(accel.get("x"), 2)
    y = math.pow(accel.get("y"), 2)
    z = math.pow(accel.get("z"), 2)

    return {
        "id": "resultant",
        "value": math.sqrt(x+y+z)
    }

def convertFilteredResult(result):
    return {
        "id": "filteredResult",
        "value": result
    }

def convertMagnitude(mag):
    return {
        "id": "fft magnitude",
        "value": mag
    }

def returnArray(object):
    return object["value"]


    
# mappings

def resolver_create_data(query):
    query.set_field("createData", create_data)

def resolver_compute_resultant(query):
    query.set_field("computeResultant", compute_resultant)

def resolver_make_butterwork_filter_mapper(query):
    query.set_field("makeButterworthFilter", make_butterworth_filter)

def resolver_lfilter_1D_mapper(query):
    query.set_field("lfilter1D", lfilter)

def resolver_compute_intensity(query):
    query.set_field("computeIntensity", compute_intensity)

def resolver_compute_impact(query):
    query.set_field("computeImpact", compute_impact)

def resolver_compute_1D_DFT(query):
    query.set_field("compute1DDFT", compute_1D_DFT)

def resolver_project_data(query):
    query.set_field("projectData", project_data)


    
# resolvers

def project_data(*_):
    with open('sample.json') as json_file:
        data = json.load(json_file)
        if(len(data)> 0):
            return data


def create_data(*_):
    pathIn = '../app/data/sample.csv'
    sampleData = pd.read_csv(pathIn)

    jsonData = []
    if(len(sampleData)>0):
        for k in range(0, len(sampleData)):
            accelKind = {
                "id": sampleData["time"].loc[k],
                "x": sampleData["acceleration_x"].loc[k],
                "y": sampleData["acceleration_y"].loc[k],
                "z": sampleData["acceleration_z"].loc[k]
            }

            jsonData.append(accelKind)
            print(len(jsonData))
        
       
        #write to file
        with open('sample.json', 'w') as outfile:
            json.dump(jsonData, outfile)
        return True
    else:
        return False

def compute_1D_DFT(*_, FFTInput, points):

    data = map(returnArray, FFTInput)
    fft = np.fft.ftt(data, n=points)
    mag = np.abs(fft)/(points/2)
    return map(convertMagnitude, mag)

def compute_impact(*_, intensity):
    if(intensity["value"]> 10):
        return {
            "id": "impact",
            "positive": True
        }
    else:
        return {
            "id": "impact",
            "postive": False
        }

def compute_intensity(*_, fftMagnitudes, filter, fftpoints):
    OI = 0
    fs = filter["filterFrequencies"]["samplingFrequency"]["value"]
    fc = filter["filterFrequencies"]["highCutOff"]["value"]
    kc = int((fftpoints/fs)* fc) + 1

    magnitudes = map(returnArray, fftMagnitudes)

    f = []
    for i in range(0, fftpoints/2):
        f.append((fs*i)/fftpoints)

    for k in range(0, kc):
        OI = OI + (magnitudes[k] * f[k])

    return {
        "id": "intensity",
        "value": OI
    }

def compute_resultant(*_, accelerations):
    return map(getResultant, accelerations) 

def make_butterworth_filter(*_, filter):
    nyq = 0.5 * filter["filterFrequencies"]["samplingFrequency"]["value"]
    low = filter["filterFrequencies"]["lowCutOff"]["value"] / nyq
    high = filter["filterFrequencies"]["highCutOff"]["value"] / nyq
    order = filter["filterOrder"]

    b, a = butter(order, [low, high], btype=filter["function"]["id"])    
    return {
        "id": filter.get("function").get("id"),
        "numerator": b,
        "denominator": a,
    }

def lfilter1D(*_, polynomials, data):
    y = lfilter(polynomials["numerator"], polynomials["denominator"], data)
    return map(convertFilteredResult, y)