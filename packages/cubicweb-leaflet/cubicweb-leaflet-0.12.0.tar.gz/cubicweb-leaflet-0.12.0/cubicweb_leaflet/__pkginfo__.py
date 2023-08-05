# pylint: disable=W0622
"""cubicweb-leaflet application packaging information"""

modname = 'leaflet'
distname = 'cubicweb-leaflet'

numversion = (0, 12, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'Cube for leaflet map, see http://leafletjs.com/'
web = 'https://forge.extranet.logilab.fr/cubicweb/cubes/%s' % distname

__depends__ = {'cubicweb': ">= 3.38.0, < 3.39.0"}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]
