# pylint: disable-msg=W0622
"""cubicweb-comment packaging information"""

modname = 'comment'
distname = "cubicweb-%s" % modname

numversion = (2, 0, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = "Logilab"
author_email = "contact@logilab.fr"
web = 'https://forge.extranet.logilab.fr/cubicweb/cubes/%s' % distname
description = "commenting system for the CubicWeb framework"
classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]

__depends__ = {'cubicweb': ">= 3.38.0, < 3.39.0"}
