from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def displayStatus():
    return 'Logchain-as-a-Service (LCaaS) has been succesfully intiated! Use our RESTful API to interact with it!'


@app.route('/verify_blocks')
def get_blocks():
    return jsonify(Circledblock)

@app.route('/submit_raw', methods=['POST'])

def set_blocks():
    print("We recieved:  " , request.get_json())
    return 'woow so cool. A new record is added successfully', 204



if __name__ == '__main__':
    app.run()
