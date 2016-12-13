#!/usr/bin/python
# -*- coding: utf-8 -*-

from plone.indexer.decorator import indexer
from ..taxonomie import ITaxonomie

@indexer(ITaxonomie)
def taxonomicTermDetails_term_rank(object, **kw):
    try:
        if hasattr(object, 'taxonomicTermDetails_term_rank'):
            return object.taxonomicTermDetails_term_rank
        else:
            return ""
    except:
        return ""

@indexer(ITaxonomie)
def taxonomie_priref(object, **kw):
    try:
        if hasattr(object, 'priref'):
            return object.priref
        else:
            return ""
    except:
        return ""

