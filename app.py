from flask import Flask, request, jsonify
from aggregate import build, Aggregate, Distortion, qd
import json


#import pandas as pd

app = Flask(__name__)

app.config["DEBUG"] = True

#app = cors(app, allow_origin="https://gpt.myinsuranceanalyst.com")


@app.route('/')
def test():
    return 'test'


@app.route('/price', methods=['GET', 'POST'])
def aggregate_start():
    """
    Build an aggregate and distortion. Then Price.

    Expects and input of the form:

        { 'agg': { arguments}, 'distortion': {args}. 'pricing': {args}}

    All of the args are optional. With this design it is easy to add more potential args.

    """
    # convert args into a dictionary
    request_data = request.get_json()

    # default data
    defaults = {

        'agg': {
            'name': 'Comm.Auto',
            'exp_en': 10,
            'exp_attachment': 0,
            'exp_limit': 10000,
            'sev_name': 'lognorm',
            'sev_mean': 50,
            'sev_cv': 4,
            'freq_name': 'poisson'},

        'distortion': {
            'name': 'dual',
            'shape': 1.94363,
            'display_name': 'myDUAL',
        },

        'pricing': {'percentile': .99}
    }

    for k, v in defaults.items():
        in_data = request_data.get(k, None)
        if in_data is not None:
            v.update(in_data)

    print(defaults)

    a = Aggregate(**defaults['agg'])
    a.update()
    qd(a)

    d = Distortion(**defaults['distortion'])

    result = a.price(defaults['pricing']['percentile'], d)

    return jsonify({'result': result.to_json()})


@app.route('/decl', methods=['GET', 'POST'])
def aggregate_run_decl():
    """
    Run a decl program.

    """
    request_data = request.get_json()
    decls = request_data.get('decl', None)

    results = {}
    if decls is not None:
        for decl in decls:
            print(decl)
            try:
                ob = build(decl)
            except ValueError as e:
                results[decl] = f'Value error {e}'
            else:
                results[decl] = ob.describe.to_json()

    return jsonify({'result': json.dumps(results)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
