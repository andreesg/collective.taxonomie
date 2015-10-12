#!/usr/bin/python
# -*- coding: utf-8 -*-

from plone.indexer.decorator import indexer
from ..taxonomie import ITaxonomie

@indexer(ITaxonomie)
def taxonomicTermDetails_term_scientificName(object, **kw):
    try:
        if hasattr(object, 'taxonomicTermDetails_term_scientificName'):
            return object.taxonomicTermDetails_term_scientificName
        else:
            return ""
    except:
        return ""
