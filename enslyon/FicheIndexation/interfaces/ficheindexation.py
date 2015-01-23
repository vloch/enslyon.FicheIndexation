from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer


class IficheIndexation(Interface):
    """Fiche Indexation Content Type"""

class IficheIndexationSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer 
       for this product.
    """
