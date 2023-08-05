"""
This module contains the base class which is used by all other class-based
route handler classes.
"""

import bottle

from . import utils


METHODS = (
    'get',
    'post',
    'put',
    'patch',
    'delete',
)


class RouteBase(object):
    """
    Base class for class-based route handlers. This class produces iterable
    objects which are initialized with request parameters, and perform the
    parameter processing and constructing the response body.

    When the response is handled by bottle, the object is iterated using the
    :py:meth:`~RouteBase.__iter__` method. Therefore, this object may be turned
    into a lazy object simply by postponing any evaluation until the the method
    is called.
    """
    #: Route name
    name = None

    #: Route path
    path = None

    #: List of plugins that should be applied
    include_plugins = None
    #: List of plugins that should be skipped
    exclude_plugins = None

    #: alias of :py:mod:`bottle` module
    bottle = bottle
    #: alias of :py:data:`bottle.request` object
    request = bottle.request
    #: alias of :py:data:`bottle.response` object
    response = bottle.response
    #: alias of :py:func:`bottle.abort`
    abort = staticmethod(bottle.abort)
    #: alias of :py:func:`bottle.redirect`
    redirect = staticmethod(bottle.redirect)
    #: alias of :py:class:`bottle.HTTPResponse`
    HTTPResponse = bottle.HTTPResponse

    def __init__(self, *args, **kwargs):
        """
        This method is invoked when the request handler is called. The default
        implementation simply stores the arguments passed to the handler, and
        initializes an empty body.

        Constructing the request body is performed in the
        :py:meth:`~RouteBase.construct_body` method, which is, in turn, called
        by :py:meth:`~RouteBase.__iter__` method when bottle attempts to cast
        the response.
        """
        self.args = args
        self.kwargs = kwargs
        self.body = []
        self.app = self.request.app
        self.config = self.request.app.config
        self.method = self.request.method.lower()
        self.is_xhr = self.request.is_xhr

    @classmethod
    def route(cls, path=None, name=None, app=None, **kwargs):
        """
        Register a route by using class' configuration. This method will take
        an optional path, optional route name, and optional app object, and
        register a route for the specified path using class properties.

        If ``path`` is not specified, a path will be obtained by invoking the
        :py:meth:`~RouteBase.get_path` class method. Similarly, if ``name`` is
        not specified, it will be obtained by invoking the
        :py:meth:`~RouteBase.get_name` class method. The default app that is
        used when ``app`` argument is missing is the Bottle's defalt app.

        The handler is registered for http verbs (e.g., GET, POST) for which a
        lower-case method name exists that matches the verb.

        List of plugins that should be applied or skipped can be specified by
        ``include_plugins`` and ``exclude_plugins`` properties respectively.
        These properties should be iterables containing the plugin names as per
        bottle API.
        """
        if not app:
            app = cls.bottle.default_app()
        path = path or cls.get_path()
        if path is None:
            raise RuntimeError('No path specified for {}'.format(cls))
        kwargs['name'] = name or cls.get_name()
        kwargs['method'] = cls.get_valid_methods()
        kwargs['apply'] = cls.include_plugins
        kwargs['skip'] = cls.exclude_plugins
        kwargs['callback'] = cls
        app.route(path, **kwargs)

    @classmethod
    def get_valid_methods(cls):
        props = dir(cls)
        return [m.upper() for m in METHODS if m in props]

    @classmethod
    def get_path(cls):
        """
        Return the value of :py:attr:`~RouteBase.path` attribute.
        """
        return cls.path

    @classmethod
    def get_generic_name(cls):
        """
        Returns a generic name that can be used for naming a route. This name
        is in the ``<module_name>:<decamelized_class_name>`` format. For
        example if we have a class that is named ``MyRoute`` in a module called
        ``beans``, the resulting generic name will be ``beans:my_route``.
        """
        return '{}:{}'.format(cls.__module__.split('.')[-1],
                              utils.decamelize(cls.__name__))

    @classmethod
    def get_name(cls):
        """
        Return the value of :py:attr:`~RouteBase.name` attribute and fall back
        on a generic name returned by :py:meth:`~RouteBase.get_generic_name`
        class method.
        """
        return cls.name or cls.get_generic_name()

    def get_method(self):
        return self.request.method.lower()

    def create_response(self):
        try:
            meth = getattr(self, self.get_method())
        except AttributeError:
            self.abort(405)
        self.body = meth(*self.args, **self.kwargs)

    def __iter__(self):
        self.create_response()
        return iter(self.body)

#: Alias for ``RouteBase``
Route = RouteBase


class NonIterableResponseMixin(object):
    """
    This mixin prevents the response data from being iterated upon byte-by-byte
    by bottle, which in case of large responses has a big performance impact,
    by wrapping the response data in a list.
    """
    def __iter__(self):
        self.create_response()
        return iter([self.body])


class NonIterableRouteBase(NonIterableResponseMixin, RouteBase):
    """
    Provides the exact same functionality as :py:class:`RouteBase`, only with
    :py:class:`NonIterableResponseMixin` included, so that large response
    bodies are returned more efficiently.
    """
    pass
