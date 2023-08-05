from collective import dexteritytextindexer
from kitconcept.richpage import _
from plone.dexterity.content import Item
from plone.namedfile import field as namedfile
from plone.supermodel.model import Schema
from zope import schema
from zope.interface import implementer


class IVideo(Schema):
    """The IVideo interface"""

    title = schema.TextLine(
        title=_("Title"),
        required=False,
    )

    description = schema.Text(
        title=_("Description"),
        required=False,
        missing_value="",
    )

    youtube_embed_url = schema.TextLine(
        title=_("Youtube embed URL"),
        description=_(
            "Sie können entweder eine Youtube video URL oder eine Playlist hinzufügen"  # noqa
        ),
        required=True,
    )

    youtube_image = namedfile.NamedBlobImage(
        title="Youtube Preview Image",
        required=False,
    )

    dexteritytextindexer.searchable("transcript_description")
    transcript_description = schema.Text(
        title=_("Transkript Beschreibung"),
        required=False,
    )

    dexteritytextindexer.searchable("transcript_title")
    transcript_title = schema.TextLine(
        title=_("Transkript Titel"),
        required=False,
    )

    transcript_file = namedfile.NamedBlobFile(
        title=_("Transkript Datei"),
        required=False,
    )


@implementer(IVideo)
class Video(Item):
    """The Video content type"""
