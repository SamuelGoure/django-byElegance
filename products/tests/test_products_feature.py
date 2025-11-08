import pytest
from rest_framework.test import APIClient
from model_bakery import baker

pytestmark = pytest.mark.django_db

def client(token=None):
    c = APIClient()
    if token:
        c.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return c

def test_categories_list_is_public():
    resp = client().get("/api/categories/")
    assert resp.status_code == 200

def test_filter_products_by_category_slug_and_in_stock():
    cat = baker.make("products.Category", name="Papeterie", slug="papeterie")
    p_ok = baker.make("products.Product", category=cat, stock=10, price="2.00")
    p_zero = baker.make("products.Product", category=cat, stock=0, price="3.00")
    other = baker.make("products.Product", stock=5, price="5.00")

    resp = client().get(
        "/api/products/?category=papeterie&in_stock=true&min_price=1&max_price=4&ordering=price"
    )
    assert resp.status_code == 200

    names = [item["name"] for item in resp.json()["results"]]
    assert p_ok.name in names
    assert p_zero.name not in names
    assert other.name not in names
