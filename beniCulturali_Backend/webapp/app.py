import random
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date 
#First, it imports the os module, which is used for interacting with the operating system, particularly for handling file paths in 
#a platform-independent way.





app = Flask(__name__)
 # this is the path to the database 
# The Flask object is then instantiated with __name__, which tells Flask where to look for resources such 
#as templates and static files.Next

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'operas.db')
#the code constructs the absolute path to a SQLite database file named operas.db. It does this by
#determining the directory of the current file (os.path.dirname(__file__)), converting it to an absolute path (os.path.abspath(...)),
#and then joining it with the database filename using os.path.join(...). This ensures that the database file is always located in the
#same directory as the script, regardless of where the script is run from.

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}' 
#The Flask application's configuration is then updated to 
#specify the database URI for SQLAlchemy. The URI uses the sqlite:/// prefix followed by the absolute path to the database file, which 
#tells SQLAlchemy to use SQLite and where to find the database.

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#The configuration option SQLALCHEMY_TRACK_MODIFICATIONS is set to False 
#to disable a feature that tracks object modifications and emits signals, which is unnecessary for most applications and can use extra memory.





db = SQLAlchemy(app)
#Finally, an instance of SQLAlchemy is created and associated with the Flask app. This sets up the ORM, allowing you to define models 
#and interact with the database using Python classes and objects instead of writing raw SQL queries.

class Opera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)

    def to_dict(self):
       return {
           'id':self.id,
           'title':self.title,
           'description':self.description,
           'creation_date':self.creation_date.isoformat() if self.creation_date else None,
           'image_url':self.image_url
    }

def seed_db(): 
    with app.app_context():
        if Opera.query.first():
            print("Database already seeded")
            return

    operas_list = [
             {
            "title": "La Nascita di Venere",
            "description": "A masterpiece housed in the Italian Museum of Naples.",
            "creation_date": "1486-01-01",
            "image_url": "https://example.com/images/venere.jpg"
        },
        {
            "title": "Il Trionfo di Galatea",
            "description": "An exquisite work representing mythological themes.",
            "creation_date": "1520-05-15",
            "image_url": "https://example.com/images/galatea.jpg"
        },
        {
            "title": "La Primavera",
            "description": "A vibrant celebration of life and rebirth from an Italian museum.",
            "creation_date": "1500-03-21",
            "image_url": "https://example.com/images/primavera.jpg"
        },
        {
            "title": "Il Sogno di Scipione",
            "description": "An evocative representation of ancient dreams and legends.",
            "creation_date": "1495-07-09",
            "image_url": "https://example.com/images/scipione.jpg"
        },
        {
            "title": "La Morte di Marat",
            "description": "A stirring portrayal of revolutionary passion preserved in a gallery.",
            "creation_date": "1793-09-13",
            "image_url": "https://example.com/images/marat.jpg"
        },
        {
            "title": "Il Bacio",
            "description": "A tender piece capturing a moment of intense emotion.",
            "creation_date": "1908-02-14",
            "image_url": "https://example.com/images/bacio.jpg"
        },
        {
            "title": "La Libertà Guidatrice del Popolo",
            "description": "An iconic representation of freedom found in Italian art.",
            "creation_date": "1830-07-14",
            "image_url": "https://example.com/images/liberta.jpg"
        },
        {
            "title": "Il Quarto Stato",
            "description": "A dynamic scene depicting modern society with deep artistic expression.",
            "creation_date": "1901-10-20",
            "image_url": "https://example.com/images/quarto_stato.jpg"
        },
        {
            "title": "La Danza",
            "description": "A glimpse of movement frozen in art, celebrated in Neapolitan institutions.",
            "creation_date": "1910-06-30",
            "image_url": "https://example.com/images/danza.jpg"
        },
        {
            "title": "Il Giuramento degli Orazi",
            "description": "A powerful narrative of loyalty and valor from Italian masters.",
            "creation_date": "1784-04-21",
            "image_url": "https://example.com/images/orazi.jpg"
        },
        {
            "title": "La Scuola di Atene",
            "description": "A monumental work embodying the spirit of philosophical inquiry.",
            "creation_date": "1511-02-15",
            "image_url": "https://example.com/images/atene.jpg"
        },
        {
            "title": "Il Ratto di Europa",
            "description": "A mythological legend rendered passionately on canvas.",
            "creation_date": "1562-08-10",
            "image_url": "https://example.com/images/europa.jpg"
        },
        {
            "title": "La Sacra Famiglia",
            "description": "An intimate portrayal of the divine family preserved in a museum.",
            "creation_date": "1475-12-25",
            "image_url": "https://example.com/images/famiglia.jpg"
        },
        {
            "title": "Il Martirio di San Sebastiano",
            "description": "A dramatic representation of martyrdom that captivates viewers.",
            "creation_date": "1525-05-05",
            "image_url": "https://example.com/images/sansebastiano.jpg"
        },
        {
            "title": "La Venaria Reale",
            "description": "A majestic work that draws visitors into Italy's royal heritage.",
            "creation_date": "1700-11-11",
            "image_url": "https://example.com/images/venaria.jpg"
        },
        {
            "title": "Il Ritorno del Figlio Prodigio",
            "description": "An emotional narrative of reconciliation and hope.",
            "creation_date": "1600-07-04",
            "image_url": "https://example.com/images/figlio_prodigio.jpg"
        },
        {
            "title": "La Conversione di San Paolo",
            "description": "A religious masterpiece venerating an important spiritual figure.",
            "creation_date": "1590-01-20",
            "image_url": "https://example.com/images/sanpaolo.jpg"
        },
        {
            "title": "Il Trionfo di Bacco",
            "description": "A festive celebration of the god of wine that radiates charm.",
            "creation_date": "1570-09-09",
            "image_url": "https://example.com/images/bacco.jpg"
        },
        {
            "title": "La Maddalena",
            "description": "A serene portrait capturing the grace of a muse in contemplation.",
            "creation_date": "1490-04-18",
            "image_url": "https://example.com/images/maddalena.jpg"
        },
        {
            "title": "Il Martirio di San Bartolomeo",
            "description": "A somber depiction of sacrifice set against a museum backdrop.",
            "creation_date": "1515-06-12",
            "image_url": "https://example.com/images/sanbartolomeo.jpg"
        }


        ]
    
    for opera in operas_list:
        opera_to_add = opera.copy()
        year,month,day = map(int, opera_to_add['creation_date'].split('-'))
        opera_to_add['creation_date'] = date(year,month,day)
        new_opera = Opera(**opera_to_add)
        db.session.add(new_opera)
    db.session.commit()
    print("db successfully seeded")



@app.cli.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    db.drop_all()
    db.create_all()
    seed_db()
    print("database Initialized.")



@app.route('/api/operas/suggestions', methods=['GET'])
def get_suggestions():
    last_search = request.args.get('last search',None)
    if last_search:
        like_pattern = f"%{last_search}%"
        correlated_operas = Opera.query.filter(
            db.or_(
                Opera.title.ilike(like_pattern),
                Opera.description.ilike(like_pattern),
                Opera.image_url.ilike(like_pattern)
            )
        ).limit(5).all()
        return jsonify([opera.to_dict() for opera in correlated_operas]),200
    else:
        all_operas = Opera.query.all()
        suggestions = random.sample(all_operas,min(5, len(all_operas)))
        return jsonify([opera.to_dict() for opera in suggestions]),200    
    
    
    
@app.route('/api/operas/search', methods=['GET'])
def search_operas():
    query = request.args.get('q','')
    if query :
        like_pattern = f'%{query}%'
        operas = Opera.query.filter(
            db.or_(
                Opera.title.ilike(like_pattern),
                Opera.description.ilike(like_pattern)
            )
        ).all()
    else:
        operas = []
    return jsonify([opera.to_dict() for opera in operas]),200

if __name__ == '__main__':
    
    app.run(debug=True)
    
#http:///127.0.0.1:5000/api/operas/suggestions
#sqlite:///127.0.0.1:5000/api/operas/suggestions