import uuid

import pytest
import requests

import config


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"


# @pytest.mark.usefixtures("restart_api")
# def test_happy_path_returns_201_and_allocated_batch(add_stock):
#     sku, othersku = random_sku(), random_sku("other")
#     earlybatch = random_batchref(1)
#     laterbatch = random_batchref(2)
#     otherbatch = random_batchref(3)
#     add_stock(
#         [
#             (laterbatch, sku, 100, "2011-01-02"),
#             (earlybatch, sku, 100, "2011-01-01"),
#             (otherbatch, othersku, 100, None),
#         ]
#     )
#     data = {"orderid": random_orderid(), "sku": sku, "qty": 3}
#     url = config.get_api_url()
#
#     r = requests.post(f"{url}/allocate", json=data)
#
#     print(r.status_code == 201)
#     assert r.status_code == 201
#     assert r.json()["batchref"] == earlybatch


@pytest.mark.usefixtures("restart_api")
def test_unhappy_path_returns_400_and_error_message():
    unknown_sku, orderid = random_sku(), random_orderid()
    data = {"orderid": orderid, "sku": unknown_sku, "qty": 20}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)
    assert r.status_code == 400
    assert r.json()["message"] == f"Invalid sku {unknown_sku}"


@pytest.mark.usefixtures("restart_api")
def test_400_message_for_out_of_stock(add_stock):
    sku, small_batch, large_order = (random_sku(), random_batchref(), random_orderid())
    add_stock([(small_batch, sku, 10, "2011-01-01")])
    data = {"orderid": large_order, "sku": sku, "qty": 20}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 400
    assert r.json()["message"] == f"Out of stock for sku {sku}"


@pytest.mark.usefixtures("restart_api")
def test_400_message_for_invalid_sku():
    unknown_sku, orderid = random_sku(), random_orderid()
    data = {"orderid": orderid, "sku": unknown_sku, "qty": 20}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)
    assert r.status_code == 400
    assert r.json()["message"] == f"Invalid sku {unknown_sku}"


def post_to_add_batch(ref, sku, qty, eta):
    url = config.get_api_url()
    r = requests.post(
        f"{url}/add_batch", json={"ref": ref, "sku": sku, "qty": qty, "eta": eta}
    )
    assert r.status_code == 201


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_201_and_allocated_batch():
    sku, other_sku = random_sku(), random_sku("other")
    early_batch = random_batchref("1")
    later_batch = random_batchref("2")
    other_batch = random_batchref("3")
    post_to_add_batch(later_batch, sku, 100, "2011-01-02")
    post_to_add_batch(early_batch, sku, 100, "2011-01-01")
    post_to_add_batch(other_batch, other_sku, 100, None)
    data = {"orderid": random_orderid(), "sku": sku, "qty": 3}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 201
    assert r.json()["batchref"] == early_batch
