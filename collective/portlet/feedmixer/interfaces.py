from plone.portlets.interfaces import IPortletDataProvider
from collective.portlet.feedmixer import FeedMixerMessageFactory as _
from zope import schema
from Products.validation import validation
from Products.ATContentTypes.interface import IATTopic
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from zope.interface import implements, Interface
from plone.z3cform.fieldsets import group, extensible

def isUrlList(data):
    verify=validation.validatorFor("isURL")
    for url in (x.strip() for x in data.split()):
        if verify(url)!=True:
            return False
    return True


class IFeedMixer(IPortletDataProvider):
    """A portlet which aggregates multiple feeds.
    """
    
    title = schema.TextLine(
            title=_(u"heading_title",
                default=u"Portlet Header"),
            description=_(u"description_title",
                default=u"Title of the rendered portlet"),
            default=u"",
            required=True)

    cache_timeout = schema.Choice(
            title=_(u"heading_cache_timeout",
                default=u"Maximum time to cache feed data"),
            description=_(u"description_cache_timeout",
                default=u""),
            default=900,
            required=True,
            vocabulary="collective.portlet.feedmixer.timeouts")

    items_shown = schema.Int(
            title=_(u"heading_items_shown",
                default=u"Number of items to display"),
            description=_(u"description_items_shown",
                default=u""),
            default=5,
            required=True)

    show_header = schema.Bool(
            title=_(u"heading_show_header",
                default=u"Show Portlet Header"),
            description=_(u"description_show_header",
                default=u""),
            default=True,
            required=True)

    show_leadimage = schema.Bool(
            title=_(u"heading_show_leadimage",
                default=u"Show Collection Lead Image"),
            description=_(u"description_show_leadimage",
                default=u""),
            default=False,
            required=True)

    show_date = schema.Bool(
            title=_(u"heading_show_date",
                default=u"Show Item Date"),
            description=_(u"description_show_date",
                default=u"Publishing date for news items, start/end date(s) for events."),
            default=True,
            required=True)

    show_event_info = schema.Bool(
            title=_(u"heading_show_event_info",
                default=u"Show additional information for events"),
            description=_(u"description_show_event_info",
                default=u"Displays When and Where titles and event location."),
            default=False,
            required=True)

    show_summary = schema.Bool(
            title=_(u"heading_show_summary",
                default=u"Show Article Summary"),
            description=_(u"description_show_summary",
                default=u""),
            default=False,
            required=True)

    show_image = schema.Bool(
            title=_(u"heading_show_image",
                default=u"Show Article Image"),
            description=_(u"description_show_image",
                default=u""),
            default=False,
            required=True)

    image_position = schema.Choice(
            title=_(u"heading_image_position",
                default=u"Image Position"),
            description=_(u"description_image_position",
                default=u""),
            default='right',
            required=True,
            vocabulary="collective.portlet.feedmixer.image_position")

    image_size = schema.Choice(
            title=_(u"heading_image_size",
                default=u"Image Size"),
            description=_(u"description_image_size",
                default=u""),
            default='small',
            required=True,
            vocabulary="collective.portlet.feedmixer.image_size")

    show_footer = schema.Bool(
            title=_(u"heading_show_footer",
                default=u"Show Portlet Footer"),
            description=_(u"description_show_footer",
                default=u""),
            default=True,
            required=True)

    alternate_footer_link = schema.TextLine(
            title=_(u"alternate_footer_link",
                default=u"Alternate Footer Link"),
            description=_(u"description_title",
                default=u"Use this URL for the 'More' link, instead of the Feedmixer generated one. Note: This will be ignored if the only source is a collection."),
            default=u"",
            required=False)

    feeds = schema.ASCII(
            title=_(u"heading_feeds",
                default=u"URL(s) for all feeds"),
            description=_(u"description_feeds",
                default=u"Enter the URLs for all feeds here, one URL per "
                        u"line. RSS 0.9x, RSS 1.0, RSS 2.0, CDF, Atom 0.3 "
                        u"and ATOM 1.0 feeds are supported."),
            required=False,
            constraint=isUrlList)

    target_collection = schema.Choice(
        title=_(u"Target collection"),
        description=_(u"Include the results of collection in the feed."),
        required=False,
        source=SearchableTextSourceBinder(
            {'object_provides': IATTopic.__identifier__},
            default_query='path:'))

    reverse_feed = schema.Bool(
            title=_(u"reverse_feed",
                default=u"Reverse"),
            description=_(u"description_title",
                default=u"Reverse order of items in feed."),
            default=False,
            required=False)   

    random = schema.Bool(
            title=_(u"random",
                default=u"Select random items"),
            description=_(u"description_title",
                default=u"If enabled, items will be selected randomly, rather than based on sort order"),
            default=False,
            required=False) 

    def entries():
        """Return feed entries for all feeds.

        The entries from all feeds will be combined in a single listed and
        sorted by publication date.
        """

class IFeedMixerRelatedItems(IFeedMixer):
    pass

class IFeedMixerSimilarItems(IFeedMixer):

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        required=True)

    show_header = schema.Bool(
        title=_(u"Show portlet header"),
        description=_(u""),
        required=False,
        default=False)

    query_portal_type = schema.Choice(
            title=_(u"heading_query_portal_type",
                default=u"Content Types"),
            description=_(u"description_query_portal_type",
                default=u"Content types to include"),
            required=False,
            vocabulary='agsci.ExtensionExtender.portlet.similar.types'
    )

    query_research_areas = schema.Bool(
        title=_(u"Search Research Areas"),
        description=_(u""),
        required=False,
        default=False)

    query_plone_tags = schema.Bool(
        title=_(u"Search Plone Tags"),
        description=_(u""),
        required=False,
        default=False)

    query_public_tags = schema.Bool(
        title=_(u"Search Public Tags"),
        description=_(u""),
        required=False,
        default=False)

    query_counties = schema.Bool(
        title=_(u"Search Counties"),
        description=_(u""),
        required=False,
        default=False)

    query_programs = schema.Bool(
        title=_(u"Search Programs"),
        description=_(u""),
        required=False,
        default=False)

    query_topics = schema.Bool(
        title=_(u"Search Topics"),
        description=_(u""),
        required=False,
        default=False)
        
    query_courses = schema.Bool(
        title=_(u"Search Course"),
        description=_(u""),
        required=False,
        default=False)
        
    query_title = schema.Bool(
        title=_(u"Search Title"),
        description=_(u""),
        required=False,
        default=False)

    limit = schema.Int(
        title=_(u"Limit"),
        description=_(u"Specify the maximum number of items to show in the "
                      u"portlet."),
        required=True,
        default=10)

    limit_radius = schema.Int(
        title=_(u"Limit Radius"),
        description=_(u"Show only events within this many miles"),
        required=True,
        default=150)

    show_dates = schema.Bool(
        title=_(u"Show dates"),
        description=_(u""),
        required=False,
        default=True)

    show_location = schema.Bool(
        title=_(u"Show location "),
        description=_(u""),
        required=False,
        default=False)

    days = schema.Int(
            title=_(u"days",
                default=u"News Item Days Filter"),
            description=_(u"If showing news items, only show those within the past X days.",
                default=u""),
            default=365,
            required=True)
