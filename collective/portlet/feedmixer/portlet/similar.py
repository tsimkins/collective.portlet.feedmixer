from collective.portlet.feedmixer.interfaces import IFeedMixerSimilarItems
from collective.portlet.feedmixer.portlet import AddForm as _AddForm
from collective.portlet.feedmixer.portlet import Assignment as _Assignment
from collective.portlet.feedmixer.portlet import EditForm as _EditForm
from collective.portlet.feedmixer.portlet import Renderer as _Renderer
from plone.memoize.instance import memoize
from zope import schema
from zope.formlib import form
from zope.interface import implements
import feedparser
from plone.app.portlets.portlets import base
from Products.CMFCore.utils import getToolByName
from collective.portlet.feedmixer import getFields as _getFields
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Acquisition import aq_chain

try:
    from zope.app.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite

def _adjustFields(context=None, fields=None):
    remove =[
                'target_collection', 
                'show_footer', 
                'show_leadimage',
                'alternate_footer_link', 
                'feeds', 
                'reverse_feed', 
                'header', 'limit', 'show_dates', 'show_location'
            ]
            
    if context:
        for i in aq_chain(context):
            if IATContentType.providedBy(i):
                portal_catalog = getToolByName(i, "portal_catalog")
                indexes = portal_catalog.indexes()
                
                for (field, index) in [
                    ('query_research_areas', 'department_research_areas'),
                    ('query_counties', 'Counties'),
                    ('query_programs', 'Topics'),
                    ('query_topics', 'Subtopiocs'),
                    ('query_courses', 'Courses'),
                    ('query_public_tags', 'Tags'),
                    ('query_plone_tags', 'Subject'),
                    ('limit_radius', 'zip_code'),
                    ]:
        
                    if index not in indexes:
                        remove.append(field)        

                break

    return _getFields(fields=fields, 
                        order=['title',  'show_header', 'cache_timeout', 'items_shown',],
                        remove=remove)


class Assignment(_Assignment):
    implements(IFeedMixerSimilarItems)

    def __init__(self, *args, **kwargs):
        base.Assignment.__init__(self, *args, **kwargs)


class AddForm(_AddForm):
    """Portlet add form.
    """

    form_fields = _getFields(IFeedMixerSimilarItems)

    def create(self, data):
        path = self.context.__parent__.getPhysicalPath()
        return Assignment(assignment_context_path='/'.join(path), **data)
        
    def adjustedFields(self):
        return _adjustFields(self.context, self.form_fields)


class EditForm(_EditForm):
    """Portlet edit form.
    """

    form_fields = _getFields(IFeedMixerSimilarItems)

    def adjustedFields(self):
        return _adjustFields(self.context, self.form_fields)

class Renderer(_Renderer):

    @property
    def allEntries(self):
    
        if self.context.isPrincipiaFolderish:
            return []

        feeds=[
            self.getFeed(url='%s/@@similar_item_rss#%s' % (self.context_path, self.portlet_hash), collection=True)
        ]

        entries=self.mergeEntriesFromFeeds(feeds)

        return entries

    @memoize
    def collection(self):
        return self.context

    @memoize
    def collection_feed(self):

        # This "old_header" logic works around the fact that
        # calling the RSS template sets the "Content-Type" header
        # to "text/xml", which causes validation errors because
        # the browser is trying to parse it as XML.

        original_header = self.request.response.getHeader('content-type')

        similar_item_rss = self.context.restrictedTraverse('@@similar_item_rss')

        feed = feedparser.parse(similar_item_rss(
                    limit=getattr(self.data, 'items_shown', ''), 
                    query_portal_type=getattr(self.data, 'query_portal_type', ''), 
                    query_counties=getattr(self.data, 'query_counties', ''), 
                    query_programs=getattr(self.data, 'query_programs', ''),
                    query_topics=getattr(self.data, 'query_topics', ''),
                    query_courses=getattr(self.data, 'query_courses', ''),
                    query_title=getattr(self.data, 'query_title', ''),
                    query_research_areas=getattr(self.data, 'query_research_areas', ''),
                    query_public_tags=getattr(self.data, 'query_public_tags', ''),
                    query_plone_tags=getattr(self.data, 'query_plone_tags', ''),
                    days=getattr(self.data, 'days', ''),
                    random=getattr(self.data, 'random', ''),
        ).encode("utf-8"))

        self.request.response.setHeader('Content-Type', original_header)

        return self.cleanFeed(feed)

    @property
    def show_footer(self):
        return False

    @property
    def available(self):
        return bool(self.entries)
