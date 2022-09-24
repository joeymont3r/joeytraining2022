

import pymongo
import certifi

from datetime import date



#Einlogdaten Mongo DB

username = "jberger"
passwort = "Trainingstagebuch2022"
client = pymongo.MongoClient("mongodb+srv://jberger:Trainingstagebuch2022@clustertt.syltzqe.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db = client.trainingsdaten

methode = ''


#Abfrage Übungen

def training(trainingsart):
    col = db.get_collection(trainingsart)
    training = list(col.find({}, {'_id':0}))

    liste = []
    durchlauf = True
    max = 0

    for dic in training:
        for key in dic:
            durchlauf = True
            #print(key) #trainingsmethode
            for key2 in dic[key]:
                
                while durchlauf == True:
                    maxkey = key2
                    durchlauf = False

                if key2 != "Gewicht":
                    summe = sum(dic[key][key2])
                    if summe >= max:
                        maxkey = key2
                        max = summe
            
                    #print(key + key2)
                    
                    #print(summe)
                    
            try:
                liste = liste + [[key, dic[key][maxkey], dic[key]["Gewicht"]]]
            except:
                liste = liste + [[key, dic[key][maxkey]]]
                    
                    
                    #liste = liste.append(dic[key][key2])
                    #print(key2) datum
                    #print(dic[key][keymax]) #Sätze/Wdh.       
    
    return liste



#Anlegen neue Übung

def neueÜbung(art, übung, gewicht):
    art = art.lower()
    gewichtstring = gewicht

    col = db.get_collection(art)
    training = list(col.find({}, {'_id':0}))

    for dic in training:
        if übung in dic:
            return "Die Übung gibt es bereits!"

        else:
            if gewicht != '0':
                sc = db.get_collection(art)
                wiederholungen = []
                datum = str(date.today())
                

                s1 = {'_id':übung, übung :{datum : wiederholungen, "Gewicht" : ['('+str(gewicht)+')'+' kg']}}
                sc.insert_one(s1)
            else:
                sc = db.get_collection(art)
                wiederholungen = []
                datum = str(date.today())

                s1 = {'_id':übung, übung :{datum : wiederholungen}}
                sc.insert_one(s1)
            
            return "Die Übung wurde angelegt."

#übunglöschen

def delUebung(liste):
    global methode
    new = liste.split(',')
    col = db.get_collection(methode)
    for uebung in new:
        col.delete_one({'_id':{'$eq' : uebung}})
        #print(finde)


#trainingsplanabfrage

def listeNeu(liste):
    global methode
    trainingsart = methode
    col2 = db.trainingsplan
    plan = col2.find_one({'plan': {'$eq' : {'art': trainingsart}}}, {'_id':0, 'plan':1})
    listeneu = []
    for dic2 in plan:
        for dic3 in plan[dic2]:
            for key in dic3:
                if key == 'plan': #dic3[key] entspricht der Trainingsplanliste
                    laenge = len(dic3[key])
                    #print(laenge)
                    for i in range(laenge):
                        listeneu = listeneu + []
                    for listen in liste:
                        for übung in dic3[key]:
                            if übung in listen:
                                index = dic3[key].index(übung)
                                #print(index)
                                listeneu.insert(index, listen)
    #print(listeneu)
    return listeneu



def trainingsplan(trainingsart):
    if trainingsart == 'ganzkörper':
        methodenListe = ['push', 'pull', 'beine']
        liste = []
        for methode in methodenListe:
            col = db.get_collection(methode)
            training = list(col.find({}, {'_id':0}))

            
            


            for dic in training:
                for key in dic:
                    max = 0
                    #print(key) #trainingsmethode
                    #print(dic[key])
                    for key2 in dic[key]:
                        #print(dic[key][key2])
                        
                        
                        
                        

                        if key2 != 'Gewicht':
                            summe = sum(dic[key][key2])
                            #print(summe)
                            if summe >= max:
                                maxkey = key2
                                max = summe
                    
                            #print(key + key2)
                        #print(maxkey)
                            
                    #print(summe)
                    wiederholungen = ''
                    erstesMal = True
                    gewicht = ''
                    erstesMalGewicht = True        
                    try:
                    
                        for satz in dic[key]["Gewicht"]:
                            if erstesMalGewicht:
                                gewicht = satz
                                erstesMalGewicht = False
                            else:
                                gewicht = gewicht + ', ' + satz
                            for satz in dic[key][maxkey]:
                                if erstesMal:
                                    wiederholungen = str(satz)
                                    erstesMal = False
                                else:
                                    wiederholungen = wiederholungen + ', ' + str(satz)

                        liste = liste + [[key, wiederholungen, gewicht]]
                    except:
                        
                        for satz in dic[key][maxkey]:
                            if erstesMal:
                                wiederholungen = str(satz)
                                erstesMal = False
                            else:
                                wiederholungen = wiederholungen + ', ' + str(satz)
                        liste = liste + [[key, wiederholungen, "/"]]
        return listeNeu(liste)

    else:
        col = db.get_collection(trainingsart)
        training = list(col.find({}, {'_id':0}))

        liste = []
        


        for dic in training:
            for key in dic:
                max = 0
                #print(key) #trainingsmethode
                #print(dic[key])
                for key2 in dic[key]:
                    #print(dic[key][key2])
                    
                    
                    
                    

                    if key2 != 'Gewicht':
                        summe = sum(dic[key][key2])
                        #print(summe)
                        if summe >= max:
                            maxkey = key2
                            max = summe
                
                        #print(key + key2)
                    #print(maxkey)
                        
                #print(summe)
                wiederholungen = ''
                erstesMal = True
                gewicht = ''
                erstesMalGewicht = True        
                try:
                
                    for satz in dic[key]["Gewicht"]:
                        if erstesMalGewicht:
                            gewicht = satz
                            erstesMalGewicht = False
                        else:
                            gewicht = gewicht + ', ' + satz
                        for satz in dic[key][maxkey]:
                            if erstesMal:
                                wiederholungen = str(satz)
                                erstesMal = False
                            else:
                                wiederholungen = wiederholungen + ', ' + str(satz)

                    liste = liste + [[key, wiederholungen, gewicht]]
                except:
                    
                    for satz in dic[key][maxkey]:
                        if erstesMal:
                            wiederholungen = str(satz)
                            erstesMal = False
                        else:
                            wiederholungen = wiederholungen + ', ' + str(satz)
                    liste = liste + [[key, wiederholungen, "/"]]
        return listeNeu(liste)

    #print(liste)


#print(trainingsplan('push'))




# def datenListe(trainingsart):
    
def getDaten():
    global methode


    if methode == 'ganzkörper':
        methoden = ['push', 'pull', 'beine']
        daten = {}
        for art in methoden:
    #methode = 'push'
            training = trainingsplan(art)
            #print(liste)
            liste = []
            for übung in range(len(training)):
                liste.append(training[übung][0])
            # print(liste)
            col = db.get_collection(art)
            
        
        
            for übung in liste:
                dic = col.find_one({'_id': übung}, {'_id':0})
                
                if dic != {}:
                    for key in dic:
                        #print(key) #übung
                        
                        datum = []
                        saetze = []
                        laenge = 0
                        datenSatz = []
                        zaehler = 0
                        for key2 in dic[key]:
                            #print(key2) #datum
                            if key2 != 'Gewicht':
                                datum.append(key2)
                                if len(dic[key][key2]) > laenge:
                                        laenge = len(dic[key][key2]) #Bestimmt die maximale Anzahl an Sätzen
                                for nummer in range(laenge):
                                        if 'Satz ' + str(nummer + 1) not in saetze:
                                            saetze.append('Satz '+ str(nummer + 1)) #definiert eine Liste in denen die Sätze augelistet sind
                                for satz in saetze:
                                        if len(datenSatz) != len(saetze):
                                            if zaehler == 0:
                                                datenSatz.append([]) #erstellt eine Liste mit Unterlisten in denen anschließend die einzelnen Satzdateneingetragen werden können
                                            else:
                                                ungezaehlt = []
                                                for anzahl in range(zaehler):
                                                    ungezaehlt.append(0)
                                                datenSatz.append(ungezaehlt)
                                #print(datenSatz)
                            
                            #for eintrag in range(laenge):
                                zaehler += 1
                                index = 0
                                for satz in dic[key][key2]:
                                    datenSatz[index].append(satz)
                                    index += 1
                        
                        daten[key] =  [saetze, datum, datenSatz]




                                #print(dic[key][key2]) #wiederholungsliste
                                

                    #print(saetze)                        
                    #print(datenSatz)

                    #print(datum)
    else:
        
    #methode = 'push'
        training = trainingsplan(methode)
        #print(liste)
        liste = []
        for übung in range(len(training)):
            liste.append(training[übung][0])
        print(liste)
        col = db.get_collection(methode)
        daten = {}
    
    
        for übung in liste:
            dic = col.find_one({'_id': übung}, {'_id':0})
            
            if dic != {}:
                for key in dic:
                    #print(key) #übung
                    
                    datum = []
                    saetze = []
                    laenge = 0
                    datenSatz = []
                    zaehler = 0
                    for key2 in dic[key]:
                        #print(key2) #datum
                        if key2 != 'Gewicht':
                            datum.append(key2)
                            if len(dic[key][key2]) > laenge:
                                    laenge = len(dic[key][key2]) #Bestimmt die maximale Anzahl an Sätzen
                            for nummer in range(laenge):
                                    if 'Satz ' + str(nummer + 1) not in saetze:
                                        saetze.append('Satz '+ str(nummer + 1)) #definiert eine Liste in denen die Sätze augelistet sind
                            for satz in saetze:
                                    if len(datenSatz) != len(saetze):
                                        if zaehler == 0:
                                            datenSatz.append([]) #erstellt eine Liste mit Unterlisten in denen anschließend die einzelnen Satzdateneingetragen werden können
                                        else:
                                            ungezaehlt = []
                                            for anzahl in range(zaehler):
                                                ungezaehlt.append(0)
                                            datenSatz.append(ungezaehlt)
                            #print(datenSatz)
                        
                        #for eintrag in range(laenge):
                            zaehler += 1
                            index = 0
                            for satz in dic[key][key2]:
                                datenSatz[index].append(satz)
                                index += 1
                    
                    daten[key] =  [saetze, datum, datenSatz]

                


                

        
    
    return daten


#print(getDaten())

#trainingsplan erstellen/updaten

def trainingsplanErstellen(liste):
    global methode
    
    new = liste.split(',')  
    col = db.trainingsplan
    
    if (col.find_one({'plan': {'$eq' : {'art': methode}}}, {'_id':0})) != None:
        pläne = col.update_one({'plan': {'$eq' : {'art': methode}}}, {"$set":{'plan': ({'art':methode},{'plan': new})}})
       
    else:
        insert = {'plan':({'art' : methode}, {'plan' : new})}
        col.insert_one(insert)

def updateÜbung(liste):
    global methode
    if methode == 'ganzkörper':
        methoden = ['push', 'pull', 'beine']
    else:
        col = db.get_collection(methode)
    #methode = 'push'
    neu = liste.split(',')
    einfügeListe = list()
    wiederholungen = list()
    
    
    for inhalt in neu:
        
        wdhEnde = False
        try:
            wiederholung = int(inhalt)
            wiederholungen.append(wiederholung)
                
        except:
            if (inhalt != neu[0]):
                wdhEnde = True
            if (wdhEnde):
                einfügeListe.append(wiederholungen)
                wdhEnde = False
                wiederholungen = []
            übung = inhalt
            
            einfügeListe.append(übung)
    
    einfügeListe.append(wiederholungen)

    for wert in einfügeListe:
        if isinstance(wert,str):
            übung = wert
        else:
            wiederholungen = wert
            print(übung)
            try:
                historie = col.find_one({'_id': übung}, {'_id':0})
                insert = historie[übung]
                #print(historie)
                insert[str(date.today())] = wiederholungen

                #print(insert)

                col.update_one({'_id' :übung}, {'$set':{übung : insert}})
            except:
                for art in methoden:
                    col = db.get_collection(art)
                    try:
                        historie = col.find_one({'_id': übung}, {'_id':0})
                        insert = historie[übung]
                        print(historie)
                        insert[str(date.today())] = wiederholungen

                        print(insert)

                        col.update_one({'_id' :übung}, {'$set':{übung : insert}})
                    except:
                        übung + ' ist keine ' +  art + 'Übung'



            
    



# printListe(liste)




def trainingsMethode(art):
    global methode
    methode = art


def getMethode():
    global methode
    return methode


# liste = 'HSP,1,2,3,One-Arm-Pull-Up (rechts),5,6,7,8'
# trainingsMethode('ganzkörper')
# updateÜbung(liste)







#kilo = 50
#print(neueÜbung('push', 'Handstandwalk', '0'))
#print(training("push"))
#print(trainingsplan("push"))
#trainingsplanErstellen('Brust, Bizeps')
#delUebung('HSP')