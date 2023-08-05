# -*- coding: utf-8 -*-

from link.middleware.core import Middleware, register_middleware

import os


@register_middleware
class FileMiddleware(Middleware):
    """
    Middleware with the same API as the
    :class:`link.middleware.http.HTTPMiddleware` but with ``file://` URI.
    """

    __protocols__ = ['file']

    def get(self):
        """
        Get content of file pointed by middleware.

        :returns: file's content
        :rtype: str
        """

        path = '{0}{1}'.format(os.sep, os.path.join(*self.path))

        with open(path) as f:
            result = f.read()

        return result

    def post(self, data):
        """
        Append data to file pointed by middleware.

        :param data: data to append
        :type data: str
        """

        path = '{0}{1}'.format(os.sep, os.path.join(*self.path))

        with open(path, 'a') as f:
            f.write(data)

    def put(self, data):
        """
        Write data to file pointed by middleware.

        :param data: data to write
        :type data: str
        """

        path = '{0}{1}'.format(os.sep, os.path.join(*self.path))

        with open(path, 'w') as f:
            f.write(data)

    def delete(self, data):
        """
        Delete file pointed by middleware.

        :param data: unused (only for API compatibility)
        """

        path = '{0}{1}'.format(os.sep, os.path.join(*self.path))

        if os.path.exists(path):
            os.remove(path)

    def options(self):
        raise NotImplementedError('Unsupported by protocol')

    def head(self):
        raise NotImplementedError('Unsupported by protocol')

    def patch(self, data):
        raise NotImplementedError('Unsupported by protocol')
