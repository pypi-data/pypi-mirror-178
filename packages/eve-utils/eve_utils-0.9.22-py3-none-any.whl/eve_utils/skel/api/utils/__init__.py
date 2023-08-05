import logging
from flask import jsonify, make_response
from flask import current_app, request


LOG = logging.getLogger('utils')

unauthorized_message = {
    "_status": "ERR",
    "_error": {
        "message": "Please provide proper credentials",
        "code": 401
    }
}


def get_db():
    return current_app.data.driver.db


def get_api():
    return current_app.test_client()


def make_error_response(message, code, issues=[], **kwargs):
    if 'exception' in kwargs:
        ex = kwargs.get('exception')
        LOG.exception(message, ex)

        if ex:
            issues.append({
                'exception': {
                    'name': type(ex).__name__,
                    'type': ".".join([type(ex).__module__, type(ex).__name__]),
                    'args': ex.args
                }
            })

    resp = {
        '_status': 'ERR',
        '_error': {
            'message': message,
            'code': code
        }
    }

    if issues:
        resp['_issues'] = issues

    return make_response(jsonify(resp), code)


def is_enabled(setting):
    return setting[0].lower() in 'yte'
    # i.e. the following means setting is enabled:
    # - 'Yes' or 'yes' or 'Y' or 'y'
    # - 'True' or 'true' or 'T' or 't'
    # - 'Enabled' or 'enabled' or 'E' or 'e'


def log_settings(log, settings):
    for setting in sorted(settings):
        key = setting.upper()
        if ('PASSWORD' not in key) and ('SECRET' not in key):
            log.info(f'{setting}: {settings[setting]}')


def echo_message():
    log = logging.getLogger('echo')
    message = 'PUT {"message": {}/"", "status_code": int}, content-type: "application/json"'
    status_code = 400
    if request.is_json:
        try:
            status_code = int(request.json.get('status_code', status_code))
            message = request.json.get('message', message)
        except ValueError:
            pass

    if status_code < 400:
        log.info(message)
    elif status_code < 500:
        log.warning(message)
    else:
        log.error(message)

    return make_response(jsonify(message), status_code)
