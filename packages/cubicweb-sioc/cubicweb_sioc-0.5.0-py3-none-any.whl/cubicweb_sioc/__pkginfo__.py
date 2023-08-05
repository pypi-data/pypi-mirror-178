# pylint: disable=W0622
"""cubicweb-sioc application packaging information"""

modname = "sioc"
distname = "cubicweb-sioc"

numversion = (0, 5, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Specific views for SIOC (Semantically-Interlinked Online Communities)"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/%s" % distname
classifiers = [
    "Framework :: CubicWeb",
    "Programming Language :: Python",
]

__depends__ = {
    "cubicweb": ">= 3.38.0, < 3.39.0",
    "six": ">= 1.4.0",
}
__recommends__ = {}
