# -*- coding: utf-8 -*-

from b3j0f.conf import Configurable, category

from link.middleware.core import Middleware
from link.json import CONF_BASE_PATH

from jsonschema import RefResolver
from jsonpointer import resolve_pointer
import json


@Configurable(
    paths='{0}/resolver.conf'.format(CONF_BASE_PATH),
    conf=category('JSONRESOLVER')
)
class JsonResolver(RefResolver):
    """
    Resolve JSON references.

    See: https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03
    """

    def __init__(self, base_uri='', referrer=None, **kwargs):
        if base_uri is None:
            base_uri = ''

        super(JsonResolver, self).__init__(base_uri, referrer, **kwargs)

        # Just make required parameters optionnal

    def resolve_remote(self, uri):
        try:
            middleware = Middleware.get_middleware_by_uri(uri)

        except Middleware.Error:
            result = super(JsonResolver, self).resolve_remote(uri)

        else:
            result = json.loads(middleware.get())

            if middleware.fragment:
                result = resolve_pointer(result, middleware.fragment)

            if self.cache_remote:
                self.store[uri] = result

        return result

    def __call__(self, ref):
        """
        Helper method for resolving.

        :return: Resolved reference
        :rtype: any
        """

        return self.resolve(ref)[1]
