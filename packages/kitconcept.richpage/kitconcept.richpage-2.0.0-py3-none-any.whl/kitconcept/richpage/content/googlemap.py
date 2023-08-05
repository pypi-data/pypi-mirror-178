from kitconcept.richpage import _
from plone.dexterity.content import Item
from zope import schema
from zope.interface import implementer
from zope.interface import Interface


class IGoogleMap(Interface):

    title = schema.TextLine(
        title=_("Title"),
        required=False,
    )

    google_map_embed_url = schema.TextLine(
        title=_("Google Map embed URL"),
        description=_(
            "1) Auf GoogleMaps gehen und in das Suchfeld eine Adresse eingeben.\n"
            '2) Auf das Teilen-Symbol klicken und dann auf "Karte einbetten" gehen.'
            "3) Es öffnet sich ein iframe-Code. Hier den Teil hinter "
            "src= zwischen den Anführungszeichen kopieren und hier einfügen."
        ),
        required=True,
    )


@implementer(IGoogleMap)
class GoogleMap(Item):
    """The GoogleMap content type"""
