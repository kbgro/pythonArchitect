from datetime import datetime

from flask import Flask, request

from src.adapters import orm
from src.domain import commands
from src.service_layer import messagebus, unit_of_work
from src.service_layer.handlers import InvalidSku

orm.start_mappers()
app = Flask(__name__)


@app.route("/add_batch", methods=["POST"])
def add_batch():
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    cmd = commands.CreateBatch(request.json["ref"], request.json["sku"], request.json["qty"], eta)
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    messagebus.handle(cmd, uow)
    return "OK", 201


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    try:
        cmd = commands.Allocate(request.json["orderid"], request.json["sku"], request.json["qty"])
        uow = unit_of_work.SqlAlchemyUnitOfWork()
        results = messagebus.handle(cmd, uow)
        batchref = results.pop(0)
    except InvalidSku as e:
        return {"message": str(e)}, 400

    return {"batchref": batchref}, 201
