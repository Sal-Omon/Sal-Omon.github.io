from flask import Flask,jsonify

app = Flask(__name__)

artifacts_list = [
    {
        "id": 1,
        "name": "La Nascita di Venere",
        "description": "A masterpiece housed in the Italian Museum of Naples.",
        "creation_date": "1486-01-01",
        "image_url": "https://example.com/images/venere.jpg"
    },
    {
        "id": 2,
        "name": "Il Trionfo di Galatea",
        "description": "An exquisite work representing mythological themes.",
        "creation_date": "1520-05-15",
        "image_url": "https://example.com/images/galatea.jpg"
    },
    {
        "id": 3,
        "name": "La Primavera",
        "description": "A vibrant celebration of life and rebirth from an Italian museum.",
        "creation_date": "1500-03-21",
        "image_url": "https://example.com/images/primavera.jpg"
    },
    {
        "id": 4,
        "name": "Il Sogno di Scipione",
        "description": "An evocative representation of ancient dreams and legends.",
        "creation_date": "1495-07-09",
        "image_url": "https://example.com/images/scipione.jpg"
    },
    {
        "id": 5,
        "name": "La Morte di Marat",
        "description": "A stirring portrayal of revolutionary passion preserved in a gallery.",
        "creation_date": "1793-09-13",
        "image_url": "https://example.com/images/marat.jpg"
    },
    {
        "id": 6,
        "name": "Il Bacio",
        "description": "A tender piece capturing a moment of intense emotion.",
        "creation_date": "1908-02-14",
        "image_url": "https://example.com/images/bacio.jpg"
    },
    {
        "id": 7,
        "name": "La Libertà Guidatrice del Popolo",
        "description": "An iconic representation of freedom found in Italian art.",
        "creation_date": "1830-07-14",
        "image_url": "https://example.com/images/liberta.jpg"
    },
    {
        "id": 8,
        "name": "Il Quarto Stato",
        "description": "A dynamic scene depicting modern society with deep artistic expression.",
        "creation_date": "1901-10-20",
        "image_url": "https://example.com/images/quarto_stato.jpg"
    },
    {
        "id": 9,
        "name": "La Danza",
        "description": "A glimpse of movement frozen in art, celebrated in Neapolitan institutions.",
        "creation_date": "1910-06-30",
        "image_url": "https://example.com/images/danza.jpg"
    },
    {
        "id": 10,
        "name": "Il Giuramento degli Orazi",
        "description": "A powerful narrative of loyalty and valor from Italian masters.",
        "creation_date": "1784-04-21",
        "image_url": "https://example.com/images/orazi.jpg"
    },
    {
        "id": 11,
        "name": "La Scuola di Atene",
        "description": "A monumental work embodying the spirit of philosophical inquiry.",
        "creation_date": "1511-02-15",
        "image_url": "https://example.com/images/atene.jpg"
    },
    {
        "id": 12,
        "name": "Il Ratto di Europa",
        "description": "A mythological legend rendered passionately on canvas.",
        "creation_date": "1562-08-10",
        "image_url": "https://example.com/images/europa.jpg"
    },
    {
        "id": 13,
        "name": "La Sacra Famiglia",
        "description": "An intimate portrayal of the divine family preserved in a museum.",
        "creation_date": "1475-12-25",
        "image_url": "https://example.com/images/famiglia.jpg"
    },
    {
        "id": 14,
        "name": "Il Martirio di San Sebastiano",
        "description": "A dramatic representation of martyrdom that captivates viewers.",
        "creation_date": "1525-05-05",
        "image_url": "https://example.com/images/sansebastiano.jpg"
    },
    {
        "id": 15,
        "name": "La Venaria Reale",
        "description": "A majestic work that draws visitors into Italy's royal heritage.",
        "creation_date": "1700-11-11",
        "image_url": "https://example.com/images/venaria.jpg"
    },
    {
        "id": 16,
        "name": "Il Ritorno del Figlio Prodigio",
        "description": "An emotional narrative of reconciliation and hope.",
        "creation_date": "1600-07-04",
        "image_url": "https://example.com/images/figlio_prodigio.jpg"
    },
    {
        "id": 17,
        "name": "La Conversione di San Paolo",
        "description": "A religious masterpiece venerating an important spiritual figure.",
        "creation_date": "1590-01-20",
        "image_url": "https://example.com/images/sanpaolo.jpg"
    },
    {
        "id": 18,
        "name": "Il Trionfo di Bacco",
        "description": "A festive celebration of the god of wine that radiates charm.",
        "creation_date": "1570-09-09",
        "image_url": "https://example.com/images/bacco.jpg"
    },
    {
        "id": 19,
        "name": "La Maddalena",
        "description": "A serene portrait capturing the grace of a muse in contemplation.",
        "creation_date": "1490-04-18",
        "image_url": "https://example.com/images/maddalena.jpg"
    },
    {
        "id": 20,
        "name": "Il Martirio di San Bartolomeo",
        "description": "A somber depiction of sacrifice set against a museum backdrop.",
        "creation_date": "1515-06-12",
        "image_url": "https://example.com/images/sanbartolomeo.jpg"
    }
]

@app.route('/api/opere', methods=['GET'])
def get_opere():
    return jsonify(artifacts_list)
 
if __name__ == '__main__':
    app.run(debug=True)
 