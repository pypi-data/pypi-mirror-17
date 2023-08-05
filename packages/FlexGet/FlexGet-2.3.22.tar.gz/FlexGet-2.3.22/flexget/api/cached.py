from __future__ import unicode_literals, division, absolute_import
from builtins import *  # pylint: disable=unused-import, redefined-builtin

from flask.helpers import send_file
from flask_restplus import inputs
from flexget.api import api, APIResource, ApiError, BadRequest
from flexget.utils.tools import cached_resource
from requests import RequestException

cached_api = api.namespace('cached', description='Cache remote resources')

cached_parser = api.parser()
cached_parser.add_argument('url', required=True, help='URL to cache')
cached_parser.add_argument('force', type=inputs.boolean, default=False, help='Force fetching remote resource')


@cached_api.route('/')
class CachedResource(APIResource):
    @api.response(200, description='Return file')
    @api.response(BadRequest)
    @api.response(ApiError)
    @api.doc(parser=cached_parser)
    def get(self, session=None):
        """ Cache remote resources """
        args = cached_parser.parse_args()
        url = args.get('url')
        force = args.get('force')
        try:
            file_path, mime_type = cached_resource(url, force)
        except RequestException as e:
            raise BadRequest('Request Error: {}'.format(e.args[0]))
        except OSError as e:
            raise ApiError('Error: {}'.format(e.args[0]))
        return send_file(file_path, mimetype=mime_type)
