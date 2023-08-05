from kitconcept.richpage import _
from plone.dexterity.content import Item
from zope import schema
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


align = SimpleVocabulary(
    [
        SimpleTerm(value="left", title=_("Left")),
        SimpleTerm(value="right", title=_("Right")),
    ]
)


class IImage(Interface):

    title = schema.TextLine(
        title=_("Title"),
        required=False,
    )

    align = schema.Choice(
        title=_("Align"),
        vocabulary=align,
        required=False,
    )


@implementer(IImage)
class Image(Item):
    """The Image content type"""
