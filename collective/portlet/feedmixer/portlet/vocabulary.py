from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.portlet.feedmixer import FeedMixerMessageFactory as _

class CacheTimeoutVocabulary(object):
    """Vocabulary factory for cache timeouts.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary([
            SimpleTerm(900, title=_(u"15 minutes")),
            SimpleTerm(1800, title=_(u"30 minutes")),
            SimpleTerm(3600, title=_(u"1 hour")),
            SimpleTerm(86400, title=_(u"24 hours")),
            ])

CacheTimeoutVocabularyFactory = CacheTimeoutVocabulary()



class ImagePositionVocabulary(object):
    """Vocabulary factory for image position.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary([
            SimpleTerm('right', title=_(u"Right")),
            SimpleTerm('left', title=_(u"Left")),
            ])

ImagePositionVocabularyFactory = ImagePositionVocabulary()

class ImageSizeVocabulary(object):
    """Vocabulary factory for image size.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary([
            SimpleTerm('small', title=_(u"Small")),
            SimpleTerm('large', title=_(u"Large")),
            ])

ImageSizeVocabularyFactory = ImageSizeVocabulary()