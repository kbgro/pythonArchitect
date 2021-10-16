from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from src.service_layer import services
from src.domain import model
from src.adapters import repository, orm
from src.adapters.orm import batches
from src.service_layer.services import is_valid_sku

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json["orderid"],
        request.json["sku"],
        request.json["qty"],
    )

    if not is_valid_sku(line.sku, batches):
        return jsonify({"message": f"Invalid sku {line.sku}"}), 400

    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    session.commit()

    return jsonify({"batchref": batchref}), 201
