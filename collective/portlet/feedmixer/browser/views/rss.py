from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.agCommon.browser.views import FolderView
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
from zope.interface import implements, Interface
import random

class RelatedItemRSSView(FolderView):

    def getFolderContents(self):
        related_item_uids = self.context.getRawRelatedItems()
        if related_item_uids:
            results = self.portal_catalog.searchResults({'UID' : related_item_uids})
            return sorted(results, key=lambda x: related_item_uids.index(x.UID))
        else:
            return []

class SimilarItemRSSView(FolderView):

    def catalog_indexes(self):
        return set(['Counties','Topics','Subtopics','Courses','Title','department_research_areas', 'Tags', 'Subject'])

    def __call__(self, 
                    limit=10, 
                    query_portal_type=None, 
                    query_counties=None, 
                    query_programs=None,
                    query_topics=None,
                    query_courses=None,
                    query_title=None,
                    query_research_areas=None,
                    query_public_tags=None,
                    query_plone_tags=None,                    
                    random=False,
                    days=365,
                    ):
        self.limit=limit
        self.query_portal_type=query_portal_type
        self.query_counties=query_counties
        self.query_programs=query_programs
        self.query_topics=query_topics
        self.query_courses=query_courses
        self.query_title=query_title
        self.query_research_areas=query_research_areas
        self.query_public_tags=query_public_tags
        self.query_plone_tags=query_plone_tags
        self.random=random
        self.days=days

        return self.index()

    def getFolderContents(self):

        similar_query = {}
        
        if self.query_portal_type:
            similar_query['portal_type'] = self.query_portal_type

            if self.query_portal_type in ['Event']:
                similar_query['sort_on'] = 'start'
                similar_query['sort_order'] = 'ascending'
                similar_query['start'] = {'query' : DateTime(), 'range' : 'min'}
                similar_query['end'] = {'query' : DateTime(), 'range' : 'min'}

            if self.query_portal_type in ['News Item']:
                similar_query['sort_on'] = 'effective'
                similar_query['sort_order'] = 'descending'
                similar_query['effective'] = {'query' : DateTime()-self.days, 'range' : 'min'}
                
        if self.query_counties and getattr(self.context, 'extension_counties', ''):
            similar_query['Counties'] = getattr(self.context, 'extension_counties', '')

        if self.query_programs and getattr(self.context, 'extension_topics', ''):
            similar_query['Topics'] = getattr(self.context, 'extension_topics', '')

        if self.query_topics and getattr(self.context, 'extension_subtopics', ''):
            similar_query['Subtopics'] = getattr(self.context, 'extension_subtopics', '')

        if self.query_courses and getattr(self.context, 'extension_courses', ''):
            similar_query['Courses'] = getattr(self.context, 'extension_courses', '')

        if self.query_title and self.context.Title():
            similar_query['Title'] = self.context.Title()
        
        if self.query_research_areas and getattr(self.context, 'department_research_areas', ''):
            similar_query['department_research_areas'] = getattr(self.context, 'department_research_areas', '')

        if self.query_public_tags and getattr(self.context, 'public_tags', ''):
            similar_query['Tags'] = getattr(self.context, 'public_tags', '')

        if self.query_plone_tags and self.context.Subject():
            similar_query['Subject'] = self.context.Subject()

        if self.context.portal_type in ['Event'] and self.query_portal_type in ['Event'] and self.limit_radius and self.limit_radius > 0:
            if hasattr(self.context, 'zip_code') and self.context.zip_code and self.context.zip_code != '00000':
                ezt = getToolByName(self.context, "extension_zipcode_tool")
                zip_codes = ezt.getNearbyZIPs(self.context.zip_code, self.limit_radius)
                search_zip_codes = set(self.portal_catalog.uniqueValuesFor('zip_code')) & set(zip_codes)
                similar_query['zip_code'] = list(search_zip_codes)


        if set(similar_query.keys()) & self.catalog_indexes():

            all_brains = self.portal_catalog.searchResults(similar_query)
            brains = []
    
            for b in all_brains:
                if b.UID != self.context.UID():
                    brains.append(b)

            if self.random and len(brains) > self.limit:
                indexes = sorted(random.sample(range(0,len(brains)), self.limit))
                brains = [brains[x] for x in indexes]
            else:            
                brains = brains[:self.limit]

            return brains

        else:
            return []
