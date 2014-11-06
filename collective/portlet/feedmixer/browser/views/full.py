from Products.Five.browser import BrowserView
from collective.portlet.feedmixer.portlet import Renderer

class FullFeedView(BrowserView):

    @property
    def title(self):
        return self.context.title

    @property
    def entries(self):
        portlet_renderer = Renderer(self.aq_acquire('context'), None, None, None, self.aq_acquire('context').data)
        return portlet_renderer.allEntries
