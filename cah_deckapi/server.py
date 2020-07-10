import json

from bottle import route, run, view, redirect, response, static_file, template, request, abort
from bottle_mongo import MongoPlugin
from bson import ObjectId
from bson.codec_options import TypeRegistry, CodecOptions

from cah.card import Card
from cah.deck import Deck
from cah.cardtype import CardType
from bson.json_util import dumps

debug = True


@route('/')
def index():
    stylesheets = []
    scripts = []
    if debug:
        scripts.append('<script src="/js/vue/vue.js"></script>')
    else:
        scripts.append('<script src="/js/vue/vue.min.js"></script>')
    scripts.append('<script src="/js/axios/axios.min.js"></script>')
    stylesheets.append('<link rel="stylesheet" href="/css/main.css">')
    return template('index', stylesheets=stylesheets, scripts=scripts)


@route('/decks/<id:path>', method='GET')
def get_deck_view(id, mongodb):
    stylesheets = []
    scripts = []
    if debug:
        scripts.append('<script src="/js/vue/vue.js"></script>')
    else:
        scripts.append('<script src="/js/vue/vue.min.js"></script>')
    scripts.append('<script src="/js/axios/axios.min.js"></script>')
    stylesheets.append('<link rel="stylesheet" href="/css/main.css">')
    deck = mongodb['decks'].find_one({"_id": ObjectId(id)})
    return template('deck_view', stylesheets=stylesheets, scripts=scripts, deck=deck)


@route('/api/v1/decks/', method='GET')
def get_decks(mongodb):
    response.content_type = "application/json"
    decks = []
    for deck in mongodb['decks'].find():
        decks.append(deck)
    if not decks:
        return dumps(json.dumps('{}'))
    return dumps(decks)


@route('/api/v1/decks/<id:path>', method='GET')
def get_deck(id, mongodb):
    response.content_type = "application/json"
    return dumps(mongodb['decks'].find_one({"_id": ObjectId(id)}))


@route('/api/v1/decks/<id:path>', method='POST')
def add_card(id, mongodb):
    deck = mongodb['decks'].find_one({"_id": ObjectId(id)})
    if deck:
        type = CardType(request.forms.get('ftype'))
        content = str(request.forms.get('fcontent'))
        pick = int(request.forms.get('fpick'))
        draw = int(request.forms.get('fdraw'))
        card = Card(type=type, content=content, pick=pick, draw=draw)
        result = mongodb['decks'].update_one({"_id": ObjectId(id)}, {'$push': {'cards': card.to_json_obj()}})
        redirect("/decks/" + id)
    else:
        return None


@route('/api/v1/decks/', method='POST')
def add_deck(mongodb):
    deck = Deck(
        name=request.forms.get('fname'),
        description=request.forms.get('fdescription'),
        lang=request.forms.get('flang')
    )
    if deck is not None:
        mongodb['decks'].insert_one(deck.to_json_obj())
        redirect('/')
    else:
        return None


@route('/js/<filename:path>', method='GET')
def send_js(filename):
    return static_file(filename, root='resources/js/')


@route('/css/<filename:path>', method='GET')
def send_css(filename):
    return static_file(filename, root='resources/css/')


if __name__ == '__main__':
    plugin = MongoPlugin(uri="mongodb://127.0.0.1", db="cah", json_mongo=True)
    run(debug=debug, host='localhost', port=8080, reloader=True, plugins=[plugin])
