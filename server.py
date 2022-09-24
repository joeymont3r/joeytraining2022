
from flask import Flask
from flask import render_template

from flask import request
from abfragen import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/push")
def push():
    trainingsMethode("push")
    return render_template('training.html', training = trainingsplan("push"), art = "push")

@app.route("/pull")
def pull():
    trainingsMethode("pull")
    return render_template('training.html', training = trainingsplan("pull"), art = "pull")

@app.route("/beine")
def beine():
    trainingsMethode("beine")
    return render_template('training.html', training = trainingsplan("beine"), art = "beine")

@app.route("/ganzkörper")
def ganzkörper():
    trainingsMethode("ganzkörper")
    return render_template('training.html', training = trainingsplan("ganzkörper"), art = "ganzkörper")



@app.route("/analyse", methods = ['POST'])
def analyse():
    try:
        liste = request.form['liste']
        updateÜbung(liste)
        methode = getMethode()
    except:
        methode = getMethode()
    training = trainingsplan(methode)
    daten = getDaten()
    return render_template('analyse.html', training = training, daten = daten)

@app.route("/neuerTrainingsplan/<methode>", methods = ['POST', 'GET'])
def neuerTrainingsplan(methode):
    if methode == 'neueuebung':
        return render_template('neueuebung.html')
    elif methode == 'uebunganlegen':
        art = request.args['art']
        übung = request.args['übung']
        gewicht = request.args['gewicht']
        return render_template('uebungerstellt.html', training = neueÜbung(art, übung, gewicht), link = art)  
    elif methode == 'erstellt':
        liste = request.form['liste']
        trainingsplanErstellen(liste)
        art = getMethode()
        return render_template('erstellt.html', link = art)
    elif methode == 'löschen':
        geloescht = request.form['del']
        delUebung(geloescht)

        art = getMethode()
        liste = training(art)
        übungsliste = []
        for übung in liste:
            übungsliste = übungsliste +[übung[0]]
        übungsliste.sort()

        return render_template('reihenfolge.html', training = übungsliste, art = art, delete = True, liste = geloescht)

    else:
        methode = getMethode()
        if methode == 'ganzkörper':
                methoden = ['push', 'pull', 'beine']
                übungslisteGes = []
                for methode in methoden:
                    liste = training(methode)
                    übungsliste = []
                    for übung in liste:
                        übungsliste = übungsliste + [übung[0]]
                    übungslisteGes = übungslisteGes + [übungsliste]
                return render_template('reihenfolgeGk.html', push = übungslisteGes[0], pull = übungslisteGes[1], beine = übungslisteGes[2], art = 'ganzkörper')
        else:
            liste = training(methode)
            übungsliste = []
            for übung in liste:
                übungsliste = übungsliste +[übung[0]]
            übungsliste.sort()
            
            
            return render_template('reihenfolge.html', training = übungsliste, art = methode)




if __name__ == "__main__":
    app.run()