def blockchain():
    return '''
    import hashlib
    import json
    from time import time
    from uuid import uuid4

    from flask import Flask, jsonify, request

    class Blockchain(object):
        def __init__(self):
            self.chain = []

            self.new_block(previous_hash=1, proof=100)

        def new_block(self, proof, previous_hash=None):

            block = {
                'index': len(self.chain) + 1,
                'timestamp': time(),
                'proof': proof,
                # 'hash': self.hash(self.new_block),
                'previous_hash': previous_hash or self.hash(self.chain[-1]),
            }


            self.chain.append(block)
            return block

        @property
        def last_block(self):
            return self.chain[-1]

        @staticmethod
        def hash(block):

            # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
            block_string = json.dumps(block, sort_keys=True).encode()
            return hashlib.sha256(block_string).hexdigest()

        def proof_of_work(self, last_proof):
            
            proof = 0
            while self.valid_proof(last_proof, proof) is False:
                proof += 1

            return proof

        @staticmethod
        def valid_proof(last_proof, proof):
            
            guess = f'{last_proof}{proof}'.encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            result = guess_hash[:4] == "0000"
            return result


    app = Flask(__name__)

    node_identifier = str(uuid4()).replace('-', '')

    blockchain = Blockchain()


    @app.route('/mine', methods=['GET'])
    def mine():
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)

        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify(response), 200


    @app.route('/chain', methods=['GET'])
    def full_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return jsonify(response), 200


    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)'''