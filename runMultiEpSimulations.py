#version qui marche pour modification du seed dans SimulationConfig.xml

from path import Path
from shutil import copyfile, copytree, rmtree
import random
from time import sleep
import os
import time
import xml.etree.ElementTree as ET

from eppy import modeleditor
from eppy.modeleditor import IDF

from energyplus_wrapper import EPlusRunner

import zipfile
import tempfile

import config

def updateZip(zipname, filename, xmlFile):
    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)

    # create a temp copy of the archive without filename            
    with zipfile.ZipFile(zipname, 'r') as zin:
        with zipfile.ZipFile(tmpname, 'w') as zout:
            #zout.comment = zin.comment # preserve the comment
            for item in zin.infolist():
                if item.filename != filename:
                    zout.writestr(item, zin.read(item.filename))

    # replace with the temp archive
    os.remove(zipname)
    os.rename(tmpname, zipname)

    # now add filename with its new data
    with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        f = open(xmlFile,'r')
        zf.writestr(filename,f.read())

def modify_SimulationConfig(IDFPATH, run):
    xmlFile = IDFPATH+'SimulationConfig.xml'#IDFPATH + 'tmp-fmus/agentFMU.fmu_FMI/SimulationConfig.xml'
    if os.path.exists(xmlFile):
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        root.find('seed').text = str(run * 989)
        tree.write(xmlFile)
    copyfile(xmlFile, IDFPATH + "/results/SimulationConfig" + str(run)+'.xml')
    updateZip(IDFPATH+'agentFMU.fmu', 'SimulationConfig.xml', xmlFile)
def heating_needs(results):
    import csv
    print("Computing heating needs from result dataframes")
    for data in results:
        if "table" in data:
            print("found table")
            table=results['table']
            Chauffage = float(table[49][13])
            print("In table.csv, %s kWh" % (Chauffage))
        return Chauffage
def moyenne_glissante_norme (valeurs, intervalle):
    indice_debut=(intervalle - 1) // 2
    liste_moyennes=valeurs[1:intervalle]
    liste_moyennes += [(0.2*valeurs[i - indice_debut]+0.3*valeurs[i - indice_debut+1]+0.4*valeurs[i - indice_debut+2]+
                    0.5*valeurs[i - indice_debut+3]+0.6*valeurs[i - indice_debut+4]+0.8*valeurs[i - indice_debut+5]+
                    valeurs[i - indice_debut+6]) / 3.8 for i in range(indice_debut, len(valeurs) - indice_debut)]
    return liste_moyennes
def overheating(result):
    print("computing overheating")
    indoor = None
    out = None
    heures_inconfort=[]
    oh = []
    for data in result:
            if "eplus" in data:
                print("found eplus.csv")
                indoor = result[data].iloc[:, [
                    "Mean Air Temperature" in col for col in result[data].columns]]
                out = result[data].iloc[:,[
                    "Outdoor Air Drybulb Temperature" in col for col in result[data].columns]]
                Text_moy_jour=[float(out[i:289+i].mean()) for i in range(0,len(out),288)]
                Text_glissantes=moyenne_glissante_norme(Text_moy_jour, 7)#moyenne glissante sur 7 jours selon la norme NF EN 16798-1
                Tconfort=[0.33*Tmoyext+18.8 for Tmoyext in Text_glissantes] # temperature de confort adaptatif selon la norme NF EN 16798-1
                for zone, area in config.zones_areas.items():
                    oh_zone=0
                    heures_inconfort_zone=0
                    indoor_zone=indoor.iloc[:,[zone in col for col in indoor.columns]]
                    T_moy_jour=[float(indoor_zone[i:289+i].mean()) for i in range(0,len(indoor_zone),288)]
                    for i in range(len(T_moy_jour)):
                        if T_moy_jour[i]>(Tconfort[i]+2):
                            oh_zone+=T_moy_jour[i]-(Tconfort[i]+2)
                            heures_inconfort_zone+=1
                    oh.append(oh_zone)
                    heures_inconfort.append(heures_inconfort_zone)
    area_tot=config.building_area
    areas=[]
    for zone,area in config.zones_areas.items():
        areas.append(area)
    oh_tot=sum([x*y for x,y in zip(areas,oh)])/area_tot  #somme pondérée par les surfaces
    heures_inconfort_tot=sum([x*y for x,y in zip(areas,heures_inconfort)])/area_tot  
    print("overheating = %s °C/h" % (oh_tot))
    print("heures inconfort = %s " % (heures_inconfort_tot))
    return heures_inconfort_tot

def runmulti(IDFPATH, EPWFILE, IDDPATH, EPLUSPATH, model_name, fmu_name, numberOfSimulations):
    idf = IDFPATH + model_name
    fmu_file = IDFPATH + fmu_name
    #Eppy initialization
    IDF.setiddname(IDDPATH)
    model = IDF(idf, EPWFILE)
    results_location=IDFPATH + "/results"
    if not os.path.exists(results_location):
        os.makedirs(results_location)

    heating_liste=[]
    comfort_liste=[]
    for run in range(0,numberOfSimulations):
        print ("running simulation" + str(run))
        start_time = time.time()
        modify_SimulationConfig(IDFPATH,run)
        runner = EPlusRunner(EPLUSPATH)
        simulation = runner.run_one(model, EPWFILE, extra_file=fmu_file)
        result=simulation.time_series
        heating = float(heating_needs(result))
        heating_liste.append(heating)
        comfort = float(overheating(result))
        comfort_liste.append(comfort)
        #p = subprocess.Popen(['C:/EnergyPlusV9-5-0/EnergyPlus.exe','-w', "CHAMBERY.epw", 'IDM_NoMASS.idf'], cwd=IDFPATH)
        #p.communicate()
        #copyfile(IDFPATH+'/eplustbl.htm', IDFPATH + "/results/eplustbl" + str(proc)+'.htm')
        #copyfile(location+'\\NoMASS.out', location + "\\results\\NoMASS" + str(run)+'.out')
        print("run %s in %s s" %(run, time.time() - start_time))
    print ("%s simulations done" %numberOfSimulations)
    with open("./results.csv", "w") as f:
        for heating, comfort in zip(heating_liste,comfort_liste):
            f.write(str(heating) +","+ str(comfort)+ "\n")
    return heating_liste,comfort_liste
    

if __name__ == "__main__":
    IDDPATH = config.IDDPATH
    EPLUSPATH = config.EPLUSPATH

    IDFPATH = "./modelNoMASS/"
    EPWFILE = IDFPATH + "CHAMBERY.epw"

    model_name = 'IDM_NoMASS.idf'
    fmu_name = "agentFMU.fmu"

    numberOfSimulations=100
    runmulti(IDFPATH, EPWFILE, IDDPATH, EPLUSPATH, model_name, fmu_name, numberOfSimulations)

    
    
    #model.run(output_directory=IDFPATH) #run from eppy
    
