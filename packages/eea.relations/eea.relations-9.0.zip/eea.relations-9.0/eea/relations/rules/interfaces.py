""" Content-Rules interfaces
"""
from zope import schema
from zope.interface import Interface
from eea.relations.config import IAsyncService
from eea.relations.config import EEAMessageFactory as _
try:
    from plone.stringinterp import interfaces
    IContextWrapper = interfaces.IContextWrapper
except (ImportError, AttributeError):
    class IContextWrapper(Interface):
        """ Context wrapper used by async events
        """


class IRelatedItemsAction(Interface):
    """ Related Items Action
    """
    transition = schema.Choice(
        title=_(u"Transition"),
        description=_(u"Select the workflow transition to attempt"),
        required=True,
        vocabulary=u"plone.app.vocabularies.WorkflowTransitions"
    )

    related_items = schema.Bool(
        title=_(u"Related items"),
        required=False,
        description=_(u"Attempt workflow transition on related items")
    )

    backward_related_items = schema.Bool(
        title=_(u"Backward references"),
        required=False,
        description=_(u"Attempt workflow transition on backward references")
    )

    if 'queueJob' in IAsyncService:
        asynchronous = schema.Bool(
            title=_(u"Asynchronous"),
            required=False,
            description=_(u"Perform action asynchronous")
        )
