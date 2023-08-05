from kitconcept.richpage import _
from plone.dexterity.content import Item
from plone.supermodel.model import Schema
from zope import schema
from zope.interface import implementer


class IText(Schema):

    title = schema.TextLine(
        title=_("Title"),
        required=False,
    )


@implementer(IText)
class Text(Item):
    """The Text content type"""
