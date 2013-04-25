from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Album, Image


def albums(request):
    list = Album.objects.all()
    return render_to_response('gallery/albums.html',
                              locals(),
                              context_instance=RequestContext(request))


def album(request, slugs):
    album = get_object_or_404(Album, slugs=slugs)
    image = Image.objects.filter(album=album)
    return render_to_response('gallery/album.html',
                              locals(),
                              context_instance=RequestContext(request))


def image(request, slugs):
    image = get_object_or_404(Image, slugs=slugs)
    return render_to_response('gallery/image.html',
                              locals(),
                              context_instance=RequestContext(request))
