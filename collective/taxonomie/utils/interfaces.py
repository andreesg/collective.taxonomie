#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.taxonomie import MessageFactory as _
from ..utils.vocabularies import _createPriorityVocabulary, _createInsuranceTypeVocabulary
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from collective.object.utils.widgets import SimpleRelatedItemsFieldWidget, AjaxSingleSelectFieldWidget
from collective.object.utils.source import ObjPathSourceBinder
from plone.directives import dexterity, form

from plone.formwidget.contenttree import UUIDSourceBinder

priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))

class ListField(schema.List):
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass

# # # # # # # # # # # # #
# Widget interface      #
# # # # # # # # # # # # #

class IFormWidget(Interface):
    pass

# # # # # # # # # # # # # #
# DataGrid interfaces     # 
# # # # # # # # # # # # # #

class ICommonName(Interface):
    commonName = schema.TextLine(title=_(u'Common name'), required=False)

class ISynonym(Interface):
    synonym = RelationList(
        title=_(u'Synonym'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=UUIDSourceBinder()
        ),
        required=False
    )
    form.widget('synonym', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

class IChildName(Interface):
    childName = RelationList(
        title=_(u'Child name'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=UUIDSourceBinder()
        ),
        required=False
    )
    form.widget('childName', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

class IPublication(Interface):
    publication = schema.TextLine(title=_(u'Publication'), required=False)
    originalDescription = schema.Bool(title=_(u'Original description'), required=False, default=False, missing_value=False)

class IExpert(Interface):
    expert = schema.TextLine(title=_(u'Expert'), required=False)

class IOtherSource(Interface):
    otherSource = schema.TextLine(title=_(u'Other source'), required=False)

class INotes(Interface):
    notes = schema.Text(title=_(u'Notes'), required=False)

    