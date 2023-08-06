##############
swagger2sphinx
##############

Swagger_ is an open specification for documenting REST APIs in JSON or YAML.
Imperfect as it is, it's de facto a standard for many API developers.

This extension lets you render your swagger.json file as a Sphinx document.
It uses `HTTP domain`_ directives for paths_ and a glossary for definitions_.

.. _Swagger: http://swagger.io/
.. _HTTP domain: https://pythonhosted.org/sphinxcontrib-httpdomain/
.. _paths: http://swagger.io/specification/#pathsObject
.. _definitions: http://swagger.io/specification/#definitionsObject


.. warning::

    This extension was created for a particular project and thus is only
    guaranteed to work with this particular project! It is very much likely
    you'll have to modify swagger-api.rst_ for your project.


*****
Usage
*****

#.  Install the extension:

    .. code-block:: shell

        $ pip install sphinxcontrib-swagger2sphinx

#.  Copy the content of swagger-api.rst_ to the file where you want
    your Swagger file rendered.

#.  Add the extension to your ``conf.py``:

    .. code-block::

        extensions = [
            'sphinxcontrib.swagger2sphinx',
            ...
        ]

#.  Specify the path to your Swagger file in ``conf.py``. It can be a local
    path or a URL:

    .. code-block:: python

        swagger2sphinx_swagger_location = "swagger.json"
        # swagger2sphinx_swagger_location = "http://example.com/swagger.json"

.. _swagger-api.rst: https://bitbucket.org/moigagoo/sphinxcontrib-swagger2sphinx/src/default/swagger-api.rst


************
Testimonials
************

Thanks to Eric Holscher for writing `an excellent blog post`_ about extending
Sphinx with Jinja2 templating.

.. _an excellent blog post: http://ericholscher.com/blog/2016/jul/25/integrating-jinja-rst-sphinx/


