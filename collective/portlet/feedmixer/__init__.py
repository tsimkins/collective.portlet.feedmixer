from zope.i18nmessageid import MessageFactory
FeedMixerMessageFactory = MessageFactory('collective.portlet.feedmixer')
from zope.formlib import form

def getFields(i=None, fields=None, order=[], remove=[]):

    def getSortOrder(v):
        if v in order:
            return order.index(v)
        else:
            return 99999

    if fields:
        all_fields = fields
    else:
        all_fields = form.Fields(i)

    all_fields = all_fields.omit(*remove)

    [x.__name__ for x in all_fields.__iter__()]
    field_ids = [x.__name__ for x in all_fields.__iter__()]
    field_ids.sort(key=lambda x: getSortOrder(x))

    return all_fields.select(*field_ids)
