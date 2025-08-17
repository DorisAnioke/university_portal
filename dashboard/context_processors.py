from .models import PortalPage

def portal_pages(request):
    """
    Adds all portal pages to the template context so navbar can loop through them.
    """
    pages = PortalPage.objects.all()
    return {'portal_pages': pages}