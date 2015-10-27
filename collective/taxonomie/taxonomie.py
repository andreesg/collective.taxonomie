#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Zope dependencies
#
from zope import schema
from zope.interface import invariant, Invalid, Interface, implements
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.fieldproperty import FieldProperty
from zope.component import getMultiAdapter

#
# Plone dependencies
#
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#
# z3c.forms dependencies
#
from z3c.form import group, field
from z3c.form.form import extends
from z3c.form.browser.textlines import TextLinesFieldWidget

#
# DataGridFields dependencies
#
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from collective.z3cform.datagridfield.blockdatagridfield import BlockDataGridFieldFactory
from collective.z3cform.datagridfield.interfaces import IDataGridField

# # # # # # # # # # # # # # # 
# Dexterity imports         # 
# # # # # # # # # # # # # # # 
from five import grok
from collective import dexteritytextindexer
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container
from plone.dexterity.browser import add, edit
from plone.app.widgets.dx import AjaxSelectFieldWidget

# # # # # # # # # # # # # # # # # #
# !taxonomie specific imports!   #
# # # # # # # # # # # # # # # # # #
from collective.taxonomie import MessageFactory as _
from .utils.vocabularies import *
from .utils.interfaces import *
from .utils.views import *

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from collective.object.utils.widgets import SimpleRelatedItemsFieldWidget, AjaxSingleSelectFieldWidget, ExtendedRelatedItemsFieldWidget
from collective.object.utils.source import ObjPathSourceBinder
from plone.directives import dexterity, form


# # # # # # # # # # # # #
# # # # # # # # # # # # #
# # taxonomie schema  # #
# # # # # # # # # # # # #
# # # # # # # # # # # # #

from plone.app.content.interfaces import INameFromTitle
class INameFromPersonNames(INameFromTitle):
    def title():
        """Return a processed title"""

class NameFromPersonNames(object):
    implements(INameFromPersonNames)
    
    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.title

class ITaxonomie(form.Schema):

    # priref
    priref = schema.TextLine(
        title=_(u'priref'),
        required=False
    )
    dexteritytextindexer.searchable('priref')


    # # # # # # # # # # # # # # #
    # Taxonomic term details    #
    # # # # # # # # # # # # # # #
    model.fieldset('taxonomic_term_details', label=_(u'Taxonomic term details'), 
        fields=['title', 'taxonomicTermDetails_term_rank',
                'taxonomicTermDetails_status_status', 'taxonomicTermDetails_status_validAcceptedName', 
                'taxonomicTermDetails_commonName', 'taxonomicTermDetails_synonym',
                'taxonomicTermDetails_hierarchy_parentName', 'taxonomicTermDetails_hierarchy_childNames',
                'taxonomicTermDetails_sourceAndDefinition_taxonAuthor', 'taxonomicTermDetails_sourceAndDefinition_description',
                'taxonomicTermDetails_sourceAndDefinition_distribution', 'taxonomicTermDetails_sourceAndDefinition_publication',
                'taxonomicTermDetails_sourceAndDefinition_expert', 'taxonomicTermDetails_sourceAndDefinition_otherSource',
                'taxonomicTermDetails_notes']
    )

    # Term
    title = schema.TextLine(
        title=_(u'Scientific name'),
        required=True
    )
    dexteritytextindexer.searchable('title')

    taxonomicTermDetails_term_rank = schema.Choice(
        title=_(u'Rank'), 
        required=True,
        vocabulary="collective.object.taxonomyrank", 
        default="No value",
        missing_value=" "
    )

    # Status
    taxonomicTermDetails_status_status = schema.Choice(
        title=_(u'Status'), 
        required=True,
        vocabulary="collective.taxonomie.status", 
        default="No value",
        missing_value=" "
    )

    taxonomicTermDetails_status_validAcceptedName = RelationList(
        title=_(u'Valid/accepted name'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Taxonomie')
        ),
        required=False
    )
    form.widget('taxonomicTermDetails_status_validAcceptedName', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    # Common name
    taxonomicTermDetails_commonName = ListField(title=_(u'Common name'),
        value_type=DictRow(title=_(u'Common name'), schema=ICommonName),
        required=False)
    form.widget(taxonomicTermDetails_commonName=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('taxonomicTermDetails_commonName')

    taxonomicTermDetails_synonym = RelationList(
        title=_(u'Synonym'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Taxonomie')
        ),
        required=False
    )
    form.widget('taxonomicTermDetails_synonym', ExtendedRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    # Hierarchy
    taxonomicTermDetails_hierarchy_parentName = RelationList(
        title=_(u'Parent name'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Taxonomie')
        ),
        required=False
    )
    form.widget('taxonomicTermDetails_hierarchy_parentName', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    taxonomicTermDetails_hierarchy_childNames = RelationList(
        title=_(u'Child name'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='Taxonomie')
        ),
        required=False
    )
    form.widget('taxonomicTermDetails_hierarchy_childNames', ExtendedRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    # Source and definition
    taxonomicTermDetails_sourceAndDefinition_taxonAuthor = schema.TextLine(
        title=_(u'Taxon author'),
        required=False
    )
    dexteritytextindexer.searchable('taxonomicTermDetails_sourceAndDefinition_taxonAuthor')

    taxonomicTermDetails_sourceAndDefinition_description = schema.TextLine(
        title=_(u'Description'),
        required=False
    )
    dexteritytextindexer.searchable('taxonomicTermDetails_sourceAndDefinition_description')

    taxonomicTermDetails_sourceAndDefinition_distribution = schema.TextLine(
        title=_(u'Distribution'),
        required=False
    )
    dexteritytextindexer.searchable('taxonomicTermDetails_sourceAndDefinition_distribution')

    taxonomicTermDetails_sourceAndDefinition_publication = ListField(title=_(u'Publication'),
        value_type=DictRow(title=_(u'Publication'), schema=IPublication),
        required=False)
    form.widget(taxonomicTermDetails_sourceAndDefinition_publication=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('taxonomicTermDetails_sourceAndDefinition_publication')

    taxonomicTermDetails_sourceAndDefinition_expert = ListField(title=_(u'Expert'),
        value_type=DictRow(title=_(u'Expert'), schema=IExpert),
        required=False)
    form.widget(taxonomicTermDetails_sourceAndDefinition_expert=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('taxonomicTermDetails_sourceAndDefinition_expert')

    taxonomicTermDetails_sourceAndDefinition_otherSource = ListField(title=_(u'Other source'),
        value_type=DictRow(title=_(u'Other source'), schema=IOtherSource),
        required=False)
    form.widget(taxonomicTermDetails_sourceAndDefinition_otherSource=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('taxonomicTermDetails_sourceAndDefinition_otherSource')

    # Notes
    taxonomicTermDetails_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(taxonomicTermDetails_notes=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('taxonomicTermDetails_notes')


# # # # # # # # # # # # # # # # # # # # #
# taxonomie declaration                 #
# # # # # # # # # # # # # # # # # # # # #

class Taxonomie(Container):
    grok.implements(ITaxonomie)
    pass

# # # # # # # # # # # # # # # # # # # # # # #
# taxonomie add/edit views                  # 
# # # # # # # # # # # # # # # # # # # # # # #

class AddForm(add.DefaultAddForm):
    template = ViewPageTemplateFile('taxonomie_templates/add.pt')
    def update(self):
        super(AddForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

class AddView(add.DefaultAddView):
    form = AddForm
    

class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('taxonomie_templates/edit.pt')
    
    def update(self):
        super(EditForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

