from flask import Flask, request
from user_similarity_calculator_app import db_readers
import os
from dotenv import load_dotenv

load_dotenv()

mongo_reader = db_readers.MongoReader(
    host=os.getenv("MONGO_HOST"),
    port=int(os.getenv("MONGO_PORT")),
    database=os.getenv("MONGO_DATABASE"),
    collection=os.getenv("MONGO_COLLECTION")
)

app = Flask(__name__)

def getSimilaritiesByWalletList(wallet_list, db_reader:db_readers.DBSimilarityReader ):
    wallet_set = set(wallet_list)
    result = [db_reader.getSimilaritiesByWallet(wallet=w) for w in wallet_set]
    # flattening result
    result = [item for sublist in result for item in sublist]
    return result

def filterByThresholds(data, lower_threshold=0, upper_threshold=1):
    return [item for item in data if (((float(item["similarity"])) >= lower_threshold) & (float(item["similarity"]) <= upper_threshold))]

def toCSV(data):
    return "/n".join(list(map(lambda x: ",".join([x["wallet_1"],x["wallet_2"],x["similarity"]]),data)))

def toJSON(data):
    return {"similarities": data}

@app.route("/similarity", methods=['GET'])
def get_similarity():
    # defaults
    wallet_list = None
    response_format = "json"
    upper_threshold = 1
    lower_threshold = 0

    if (request.args and "wallet_list" in request.args):
        wallet_list = request.args.get("wallet_list").split(",")

    if (request.args and "upper_threshold" in request.args):
        upper_threshold = float(request.args.get("upper_threshold"))

    if (request.args and "upper_threshold" in request.args):
        lower_threshold = float(request.args.get("lower_threshold"))

    if (request.args and "response_format" in request.args):
        response_format = request.args.get("response_format")

    global mongo_reader

    result = getSimilaritiesByWalletList(wallet_list, mongo_reader)

    result = filterByThresholds(result, lower_threshold, upper_threshold)

    if (response_format == "json"):
        result = toJSON(result)

    if (response_format == "csv"):
        result = toCSV(result)

    return result