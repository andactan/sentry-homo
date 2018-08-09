from flask import Flask, request
from raven import breadcrumbs
from raven.contrib.flask import Sentry


app = Flask(__name__)
sentry = Sentry()

SENTRY_CONFIG = {
    'dsn': 'https://3013fd71ca9641078f34f3c9d4fd262f:ddd37a1cc8e04b728bdec6f7202c5ca2@sentry.io/1259283',
    'release': '1.0'
}

app.config['SENTRY_CONFIG'] = SENTRY_CONFIG
sentry.init_app(app)

@app.route('/')
def hello():

    breadcrumbs.record(message='Hey, me looking for number')
    dividend = request.args.get('dividend')
    divisor = request.args.get('divisor')
    breadcrumbs.record(message='OK, me got the nummers')
    breadcrumbs.record(message='Wow, such message, much importance',
                       level='info')

    dividend = int(dividend)
    divisor = int(divisor)

    if divisor == 0:
        return '0'

    try:
        return str(int(dividend)/int(divisor))
    except:
        sentry.captureException()
        return 'BOOM'

if __name__ == '__main__':
    app.run()