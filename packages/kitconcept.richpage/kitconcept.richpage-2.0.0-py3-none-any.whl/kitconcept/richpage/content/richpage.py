from collective import dexteritytextindexer
from kitconcept.richpage import _
from plone.dexterity.content import Container
from plone.supermodel.model import Schema
from zope import schema
from zope.interface import implementer


class IRichPage(Schema):

    title = schema.TextLine(
        title=_("Title"),
        required=True,
    )

    dexteritytextindexer.searchable("subtitle")
    subtitle = schema.TextLine(
        title=_("Subtitle"),
        required=False,
    )

    description = schema.Text(
        title=_("Description"),
        required=False,
        missing_value="",
    )


@implementer(IRichPage)
class RichPage(Container):
    """The RichPage content type"""
