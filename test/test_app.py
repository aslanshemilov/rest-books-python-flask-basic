import pytest
from books.app import app, fake_db

isbn = "02345678"

book = {"author": "Virginia Woolf", "isbn": isbn, "title": "The Waves"}


@pytest.fixture()
def test_app():
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here
    fake_db.clear()

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(test_app):
    return test_app.test_client()


@pytest.fixture()
def runner(test_app):
    return test_app.test_cli_runner()


def test_create_book_returns_http_201_created(client):
    response = _put_book(client, isbn, book)
    assert response.status_code == 201


def _put_book(client, isbn, book):
    return client.put(f"/books/{isbn}", json=book)


def test_read_retrieve_not_exists_returns_http_404(client):
    response = client.get(f"/books/{isbn}")
    assert response.status_code == 404


def test_read_retrieve_exists_returns_book_http_200(client):

    _put_book(client, isbn, book)

    response = _get_book(client, isbn)
    assert response.status_code == 200
    assert response.json == book


def _get_book(client, isbn):
    return client.get(f"/books/{isbn}")


def test_read_list_empty_returns_http_200(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json == []


def test_read_list_returns_books_http_200(client):

    _put_book(client, isbn, book)

    response = client.get("/books")
    assert response.status_code == 200
    assert response.json == [book]


def test_update_returns_http_200(client):
    response = _put_book(client, isbn, book)
    assert response.status_code == 201

    response = _get_book(client, isbn)
    assert response.json == book

    updated_book = book.copy()
    updated_book["title"] = "Test Book"

    response = _put_book(client, isbn, updated_book)
    assert response.status_code == 200

    response = _get_book(client, isbn)
    assert response.json == updated_book


def test_delete_returns_http_404_book_not_exist(client):
    response = client.delete(f"/books/{isbn}")
    assert response.status_code == 404


def test_delete_returns_http_204_on_delete(client):
    _put_book(client, isbn, book)

    response = client.delete(f"/books/{isbn}")
    assert response.status_code == 204

    response = _get_book(client, isbn)
    assert response.status_code == 404
