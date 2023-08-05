from collective.dexteritytextindexer.utils import searchable
from plone.app.contenttypes.behaviors.richtext import IRichTextBehavior


searchable(IRichTextBehavior, "text")
