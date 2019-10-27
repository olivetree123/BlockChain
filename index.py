from flask import Flask, request
from flask_restful import Resource, Api, marshal_with

from chain import blockChain
from utils.response import APIResponse, resource_fields


app = Flask(__name__)
api = Api(app)


# 获取完整的区块链
class FullChainEndpoint(Resource):
    decorators = [marshal_with(resource_fields)]

    def get(self):
        return APIResponse(data=blockChain.blocks)


# 挖矿
class MineEndpoint(Resource):
    decorators = [marshal_with(resource_fields)]

    def post(self):
        params = request.get_json()
        if not (params and params["proof"]):
            return {}
        status = blockChain.validate_proof(params["proof"])
        if not status:
            return {}
        block = blockChain.transction("system", "you", 1)
        return APIResponse(data=block.json())


# 交易
class TransactionEndpoint(Resource):
    decorators = [marshal_with(resource_fields)]

    def post(self):
        pass


api.add_resource(FullChainEndpoint, "/chain/full", strict_slashes=False)
api.add_resource(MineEndpoint, "/chain/mine", strict_slashes=False)
api.add_resource(TransactionEndpoint, "/chain/transaction", strict_slashes=False)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
    