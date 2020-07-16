import json
import os

from bottle import route, run, response, static_file, template, request
from bottle_mongo import MongoPlugin
from bson import ObjectId
from bson.json_util import dumps
from iso639 import languages

from cah.card import Card
from cah.cardtype import CardType
from cah.deck import Deck

debug = True


@route('/')
def index():
    stylesheets = []
    scripts = []
    stylesheets.append('<link rel="stylesheet" href="/css/main.css">')
    lang = languages.part1
    return template('index', stylesheets=stylesheets, scripts=scripts, languages=lang)


@route('/decks/<id:path>', method='GET')
def get_deck_view(id):
    stylesheets = []
    scripts = []
    stylesheets.append('<link rel="stylesheet" href="/css/main.css">')
    return template('deck_view', stylesheets=stylesheets, scripts=scripts, deck_id=id)


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
    response.content_type = "application/json"
    deck = mongodb['decks'].find_one({"_id": ObjectId(id)})
    if deck:
        # noinspection PyBroadException
        try:
            type = CardType(request.json['type'])
            content = str(request.json['content'])
            pick = int(request.json['pick'])
            draw = int(request.json['draw'])
            card = Card(type=type, content=content, pick=pick, draw=draw)
            result = mongodb['decks'].update_one({"_id": ObjectId(id)}, {'$push': {'cards': card.to_json_obj()}})
            if not result.acknowledged:
                response.status = 500
                return '{"status": "nok", "error": "Unknown error upon inserting"}'
            else:
                return '{"status": "ok"}'
        except:
            response.status = 500
            return '{"status": "nok", "error": "Unknown error upon inserting"}'
    else:
        response.code = 404
        return '{"status": "nok", "error": "Deck not found"}'


@route('/api/v1/decks/', method='POST')
def add_deck(mongodb):
    response.content_type = "application/json"

    deck = None
    # noinspection PyBroadException
    try:
        deck = Deck(
            name=request.json['name'],
            description=request.json['description'],
            lang=request.json['lang'],
            cards=request.json['cards']
        )
    except:
        response.status = 400
        return '{"status": "nok", "error": "Invalid deck submitted"}'
    if deck is not None:
        result = mongodb['decks'].insert_one(deck.to_json_obj())
        if not result.acknowledged:
            response.status = 500
            return '{"status": "nok", "error": "Unknown error upon inserting"}'
        else:
            return '{"status": "ok", "id": "' + str(result.inserted_id) + '"}'


@route('/api/v1/decks/<id:path>', method='DELETE')
def delete_deck(id, mongodb):
    response.content_type = "application/json"
    result = mongodb['decks'].delete_one({'_id': ObjectId(id)})
    if result.acknowledged:
        response.code = 202
        return '{"status": "ok", "id": "' + str(id) + '"}'
    else:
        response.code = 404
        return '{"status": "nok", "error": "Deck not found"}'


@route('/js/<filename:path>', method='GET')
def send_js(filename):
    return static_file(filename, root='resources/js/')


@route('/css/<filename:path>', method='GET')
def send_css(filename):
    return static_file(filename, root='resources/css/')


@route('/favicon/<filename:path>', method='GET')
def send_css(filename):
    return static_file(filename, root='resources/favicon/')


if __name__ == '__main__':
    """ Default values """
    server_address = "0.0.0.0"
    server_port = 0
    mongodb_address = "127.0.0.1"
    mongodb_port = 27017
    mongodb_db = "cah"
    """ Try reading configuration from the environment """
    if os.environ.get('DECKAPI_ADDRESS'):
        server_address = os.environ.get('DECKAPI_ADDRESS')
    if os.environ.get('DECKAPI_PORT'):
        server_port = int(os.environ.get('DECKAPI_PORT'))
    if os.environ.get('DECKAPI_MONGODB_ADDRESS'):
        mongodb_address = os.environ.get('DECKAPI_MONGODB_ADDRESS')
    if os.environ.get('DECKAPI_MONGODB_PORT'):
        mongodb_port = int(os.environ.get('DECKAPI_MONGODB_PORT'))
    if os.environ.get('DECKAPI_MONGODB_DB'):
        mongodb_db = os.environ.get('DECKAPI_MONGODB_DB')
    if os.environ.get('DECKAPI_DEBUG'):
        debug = bool(os.environ.get('DECKAPI_DEBUG'))

    plugin = MongoPlugin(uri="mongodb://" + mongodb_address + ":" + str(mongodb_port), db=mongodb_db, json_mongo=True)
    run(debug=debug, host=server_address, port=server_port, reloader=True, plugins=[plugin])
