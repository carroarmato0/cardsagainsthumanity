import json
import ntpath
import os
import re
import tempfile
from json import JSONDecodeError

import bottle
from bottle import response, static_file, template, request, Bottle
from bottle_mongo import MongoPlugin
from bson import ObjectId
from bson.json_util import dumps
from iso639 import languages

from cah.card import Card
from cah.cardtype import CardType
from cah.deck import Deck
from cah_deckapi.CorsPlugin import EnableCORS

debug = True

consistent_underscore_regex = r"(?<=(\$|\s))(_+)(?!\w)"

app = Bottle()
package_root = os.path.dirname(os.path.realpath(__file__))


def conform_content(text):
    result = ""
    """ Trim """
    result = text.strip()
    """ End punctuation """
    if result[-1] not in ('?', '!', '.', '¡', '¿'):
        result = result + "."
    """ Shorten blank characters (_) """
    if "_" in result:
        result = re.sub(consistent_underscore_regex, "____", result, 0, re.MULTILINE | re.DOTALL)
    return result


@app.route('/')
def index():
    stylesheets = []
    scripts = []
    stylesheets.append('<link rel="stylesheet" href="/css/main.css">')
    lang = languages.part1
    return template('index', stylesheets=stylesheets, scripts=scripts, languages=lang)


@app.route('/decks/<id:path>', method='GET')
def get_deck_view(id):
    stylesheets = []
    scripts = []
    stylesheets.append('<link rel="stylesheet" href="/css/main.css">')
    return template('deck_view', stylesheets=stylesheets, scripts=scripts, deck_id=id)


@app.route('/api/v1/decks/', method='GET')
def get_decks(mongodb):
    response.content_type = "application/json"
    decks = []
    for deck in mongodb['decks'].find():
        decks.append(deck)
    if not decks:
        return dumps([])
    return dumps(decks)


@app.route('/api/v1/decks/<id:path>', method='GET')
def get_deck(id, mongodb):
    response.content_type = "application/json"
    return dumps(mongodb['decks'].find_one({"_id": ObjectId(id)}))


@app.route('/api/v1/decks/import', method='POST')
def import_decks(mongodb):
    response.content_type = "application/json"

    '''' Try to convert the payload to JSON '''
    json_request = None
    try:
        json_request = request.json
    except JSONDecodeError:
        response.status = 400
        return '{"status": "nok", "error": "Malformed JSON"}'

    ''' Check if we're dealing with an array or single submission '''
    ''' Single JSON -> dict, JSON array -> list of dicts '''
    ''' Force dict to list to simplify code '''
    if isinstance(json_request, dict):
        json_request = [json_request]

    ''' Check for empty payload '''
    if len(json_request) == 0:
        response.status = 400
        return '{"status": "nok", "error": "Invalid deck submitted"}'

    decks = []

    ''' Loop through objects and test for correctness '''
    for entry in json_request:
        # noinspection PyBroadException
        try:
            ''' Attempt to create a Deck object '''
            ''' cards initially empty because we are going to evaluate them in the next step '''
            deck = Deck(
                name=entry['name'],
                description=entry['description'],
                lang=entry['lang'],
                cards=[]
            )

            ''' Attempt to create Card objects '''
            if len(entry['cards']) > 0:
                for card_entry in entry['cards']:
                    card = Card(
                        type=CardType(card_entry['type']),
                        content=conform_content(str(card_entry['content'])),
                        pick=int(card_entry['pick']),
                        draw=int(card_entry['draw'])
                    )
                    deck.cards.append(card)

            ''' Looks fine, we add it to the validated decks list '''
            decks.append(deck)
        except:
            response.status = 400
            return '{"status": "nok", "error": "Invalid deck submitted"}'

    if decks is not None and len(decks) > 0:
        deck: Deck
        result = mongodb['decks'].insert_many(deck.to_json_obj() for deck in decks)
        if not result.acknowledged:
            response.status = 500
            return '{"status": "nok", "error": "Unknown error upon inserting"}'
        else:
            id_list = []
            for id in result.inserted_ids:
                id_list.append(str(id))
            return '{"status": "ok", "ids": ' + json.dumps(id_list) + '}'


@app.route('/api/v1/decks/export', method='GET')
def export_decks(mongodb):
    decks = list(mongodb['decks'].find({}, {"_id": 0}))
    with tempfile.NamedTemporaryFile(delete=True) as file:
        file.seek(0)
        file.write(bytes(dumps(decks), 'UTF-8'))
        file.flush()
        return static_file(ntpath.basename(file.name), root='/tmp/', download="decks-export.json")


@app.route('/api/v1/decks/<id:path>', method='POST')
def add_card(id, mongodb):
    response.content_type = "application/json"
    deck = mongodb['decks'].find_one({"_id": ObjectId(id)})
    if deck:
        # noinspection PyBroadException
        try:
            type = CardType(request.json['type'])
            content = conform_content(str(request.json['content']))
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


@app.route('/api/v1/decks/<deck_id>/cards', method='DELETE')
def delete_card(deck_id, mongodb):
    response.content_type = "application/json"
    deck = mongodb['decks'].find_one({"_id": ObjectId(deck_id)})
    if deck:
        '''' Try to convert the payload to JSON '''
        json_request = None
        try:
            json_request = request.json
        except JSONDecodeError:
            response.status = 400
            return '{"status": "nok", "error": "Malformed JSON"}'

        card = None
        try:
            ''' Attempt to create a Card object '''
            card = Card(
                type=CardType(json_request['type']),
                content=str(json_request['content']),
                pick=int(json_request['pick']),
                draw=int(json_request['draw'])
            )
        except:
            response.status = 400
            return '{"status": "nok", "error": "Malformed Card"}'

        result = mongodb['decks'].update_one({"_id": ObjectId(deck_id)}, {'$pull': {'cards': card.to_json_obj()}})
        if not result.acknowledged:
            response.status = 500
            return '{"status": "nok", "error": "Unknown error upon deleting"}'
        else:
            return '{"status": "ok"}'
    else:
        response.code = 404
        return '{"status": "nok", "error": "Deck not found"}'


@app.route('/api/v1/decks/', method='POST')
def add_deck(mongodb):
    response.content_type = "application/json"

    '''' Try to convert the payload to JSON '''
    json_request = None
    try:
        json_request = request.json
    except JSONDecodeError:
        response.status = 400
        return '{"status": "nok", "error": "Malformed JSON"}'

    deck = None
    # noinspection PyBroadException
    try:
        deck = Deck(
            name=json_request['name'],
            description=json_request['description'],
            lang=json_request['lang'],
            cards=json_request['cards']
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


@app.route('/api/v1/decks/<id:path>', method='DELETE')
def delete_deck(id, mongodb):
    response.content_type = "application/json"
    result = mongodb['decks'].delete_one({'_id': ObjectId(id)})
    if result.acknowledged:
        response.code = 202
        return '{"status": "ok", "id": "' + str(id) + '"}'
    else:
        response.code = 404
        return '{"status": "nok", "error": "Deck not found"}'


@app.route('/js/<filename:path>', method='GET')
def send_js(filename):
    return static_file(filename, root=package_root + '/resources/js/')


@app.route('/css/<filename:path>', method='GET')
def send_css(filename):
    return static_file(filename, root=package_root + '/resources/css/')


@app.route('/favicon/<filename:path>', method='GET')
def send_favicon(filename):
    return static_file(filename, root=package_root + '/resources/favicon/')


if __name__ == '__main__':
    """ Default values """
    server_address = "0.0.0.0"
    server_port = 8080
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

    mongo_plugin = MongoPlugin(uri="mongodb://" + mongodb_address + ":" + str(mongodb_port), db=mongodb_db, json_mongo=True)
    cors_plugin = EnableCORS()
    bottle.TEMPLATE_PATH.insert(0, package_root + "/views")
    app.run(debug=debug, host=server_address, port=server_port, reloader=True, plugins=[mongo_plugin, cors_plugin])
