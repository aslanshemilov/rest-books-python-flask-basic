from flask import Flask, request, Response, jsonify

app = Flask(__name__)

fake_db = {}


@app.route("/books", methods=["GET"])
@app.route("/books/<isbn>", methods=["PUT", "GET", "DELETE"])
def books(isbn=None):
    if request.method == "PUT":
        payload = request.json
        isbn = payload["isbn"]
        if isbn in fake_db:
            fake_db[isbn] = payload
            return Response(status=200)
        else:
            fake_db[isbn] = payload
            return Response(status=201)

    elif request.method == "DELETE":
        if isbn in fake_db:
            fake_db.pop(isbn)
            return Response(status=204)
        else:
            return Response(status=404)

    else:
        if isbn:
            book = fake_db.get(isbn)
            if book:
                return jsonify(book)
            else:
                return Response(status=404)
        else:
            return jsonify(list(fake_db.values()))
