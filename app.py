"""
Source : 
Date : 10/03/2020
Auteur : Christian Doriath
Dossier : /Python34/MesDEv/Flask/Flask_File_Upload
Fichier : app.py
Description : app pour envoyer des fichiers au serveur
Mot cles : flaskFileUploader flaskServerError
"""
import googleapiclient.discovery
import datetime
import string
from flask import Flask, request, render_template, session, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateTimeField
from wtforms.validators import DataRequired,Regexp,IPAddress,Length,Required,InputRequired
from wtforms.validators import Email ,Regexp, EqualTo, NumberRange, NoneOf, URL, AnyOf 
#List of available validators : http://wtforms.simplecodes.com/docs/0.6.1/validators.html
from flask_sqlalchemy import SQLAlchemy
from random import choice
import locale
import time
import pdb
import json 
from flask_debugtoolbar import DebugToolbarExtension
#import email_validator


#mardi 13 février 2024 !!!

#bipbip carotte !!!

locale.setlocale(locale.LC_TIME,'')

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hard to guess string'
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://MissPandinou:clairePapa2021@MissPandinou.mysql.eu.pythonanywhere-services.com/MissPandinou$missPandinou'

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://root:root@localhost/relation_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)

print("ma DB:",db)




class tabCodeBase(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resumeEntete = db.Column(db.String(80))
    dateCreation = db.Column(db.String(80))
    auteur = db.Column(db.String(80))
    description = db.Column(db.String(80))
    termine = db.Column(db.String(80))
    btnEdit =  db.Column(db.String(80))



db.create_all()


class tabCode(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codeHTML = db.Column(db.String(1000))
    codeJavascript = db.Column(db.String(1000))

db.create_all()




@app.route('/',methods = ['POST', 'GET'])
def mymapage():
    return render_template('index.html')

@app.route('/page',methods = ['POST', 'GET'])
def mypage():
    result = tabCodeBase.query.filter_by().all()
    print("result long:",len(result))
    liste = [] 

    if request.method == "POST":
        maValeur = tabCodeBase(
            resumeEntete= request.form["resume"],
            dateCreation = request.form["dateDeCreation"],
            auteur=request.form["auteur"],
            description=request.form["description"],
            termine=request.form["termine"],
            btnEdit=request.form["btnEdit"]
            )
        db.session.add(maValeur)
        db.session.commit()
        print("les informations ont été ajoutés !!!! ")

        for ligne in result :
            dict = {'id':ligne.id,'resumeEntete':ligne.resumeEntete,'dateCreation':ligne.dateCreation,'auteur':ligne.auteur,'description':ligne.description,'termine':ligne.termine,'btnEdit':ligne.btnEdit}  
            liste.append(dict)
            print("Voici la liste: ",liste)
            

    return render_template('page.html',data=liste)
    #,data=liste)

@app.route('/mapage4')
def mymapage4():
    return render_template('mapage4.html')
  

@app.route('/valeurs2_create',methods = ['POST', 'GET'])
def myvaleurs2():
    if request.method == "POST":
        maValeur = Valeurs2(
            resume= request.form["resume"],
            dateDeCreation = request.form["dateDeCreation"],
            auteur=request.form["auteur"],
            description=request.form["description"],
            termine=request.form["termine"],
            btnEdit=request.form["btnEdit"]
            )
        db.session.add(maValeur)
        db.session.commit() 
        print("les informations ont été ajoutés !!!! ")

        #return("les informations ont été ajoutés !!!!")
        return render_template('valeurs2_create.html')
        #return redirect(url_for("user_detail", id=maValeur.id))     
        
    
    #return ('ok ajouté')
    return render_template('create.html')


@app.route('/valeurs2_searchId/<p_id>',methods = ['POST', 'GET'])
def myvaleurs2_searchId(p_id):
    print("ID : ",p_id)
    record = Valeurs2.query.filter_by(id=p_id).first()
    print("Record est de type ",type(record))

    if record is None:
        # aucune ligne n'a été retournée 
        print("ID n'existe PAS !")
        return ("ID n'existe PAS !")
    else :
        print("Prenom:",record.prenom)
        return 'le prenom est '+record.prenom


@app.route('/valeurs2_retrieveNom',methods = ['POST', 'GET'])
def valeurs2_retrieveNom():

    if request.method == "POST":
        #on s'assure que 'request' arrive avec de la data du form
        d= request.form.to_dict()
        print("Voici les datas du formulaire :",d)
        monNom = request.form['nom']
        print("monNom :",monNom)
        #record = Valeurs2.query.filter_by(nom=p_nom).first()
        record = Valeurs2.query.filter_by(nom=monNom).all()
        # lignes = Valeurs2.query.filter(Valeurs2.nom.like(monNom)).all() 
        # print(" lignes:",lignes)

        print("type record:",type(record))
        print(" record:",record)
        print("1 record:",record[0])
        print("1 record type:",type(record[0]))
        print("1 record nom:",record[0].nom)
        

        records = []
        for elem in record :
            dict = {'nom': elem.nom ,'prenom': elem.prenom,'id':elem.id}
            records.append(dict)        
        print(jsonify(records))

        # return record 
    return render_template('valeurs2_nom.html',mesLignes=records)


# 27/03/2023
@app.route('/youtubelink',methods = ['POST', 'GET'])
def f_youtubelink():
    print("youtubelink")
    return render_template('youtubeLink01.html')

# 27/03/2023
@app.route('/youtubeApiTitle/<videoId>',methods = ['POST', 'GET'])
def f_youtubeApiTitle(p_videoId):
    # 1) récupérer la data transmise par la requête FETCH
    #URL passée = https://www.youtube.com/watch?v=170Mx8KuURM

    # 2) extraire l'ID de l'URL (dernière partie) : 170Mx8KuURM

    ID = "FFmGynQORkY"
    #ID = request.form['lienYoutube']
    print("ID:",ID)

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCmrYPCkFMvwQ9WyJp2bvGRlzrJwvg9JWM"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

    #request body 
    #URL of video : https://www.youtube.com/watch?v=170Mx8KuURM

    request = youtube.videos().list(
        part = 'snippet',
        id = ID #voir ligne 12 la fin de l'URL
    )

    #executer la requête 
    response = request.execute()

    print("Toutes les infos sont : ",response['items'])

    print("\n")

    titre = response['items'][0]['snippet']['title']
    print("Le titre est : ",titre)

    return jsonify(titre) 



@app.route('/page2',methods = ['POST', 'GET'])
def f_page2():
    print("page2")
    return render_template('page2.html')



@app.route('/page2Data',methods = ['POST', 'GET'])
def mypage2Data():
    maListe2 = []
    lignes = tabCode.query.filter_by().all()
    print("Voici les lignes trouvées :  ",lignes)
    for elem in lignes :
        dict = {'codeHTML': elem.codeHTML ,'codeJavascript': elem.codeJavascript}
        maListe2.append(dict)
        print("!!!!!!!!!!!!!!! Ma liste2:",maListe2)

    return jsonify(maListe2)

