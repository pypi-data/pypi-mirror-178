from plone.app.contenttypes import _
from plone.app.contenttypes.content import File
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IFile(model.Schema):
    """The IFile interface"""

    title = schema.TextLine(
        title=_("Title"),
        required=False,
    )

    description = schema.Text(
        title=_("Description"),
        required=False,
        missing_value="",
    )

    model.primary("file")
    file = namedfile.NamedBlobFile(
        title=_("label_file"),
        required=True,
    )

    alternate_filename = schema.TextLine(
        title=_("Datei-Titel"),
        required=False,
    )


@implementer(IFile)
class File(File):
    """The File content type"""
