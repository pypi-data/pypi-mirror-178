# pylint: disable=W0622
"""cubicweb-simplefacet application packaging information"""


modname = "simplefacet"
distname = "cubicweb-simplefacet"

numversion = (2, 0, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Cube adding another display for facets."
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/%s" % distname

__depends__ = {"cubicweb": ">= 3.38.0, < 3.39.0"}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
]
