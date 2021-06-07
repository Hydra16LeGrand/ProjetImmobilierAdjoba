from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    # url(r'^$|^acheter-lister$', view = views.Acheter.lister, name='acheter_lister'),
    # url(r'^acheter/infos-supplementaire/$', view = views.Acheter.infos_supplementaire, name='acheter_infos_supplementaire'),
    # url(r'^acheter/acheter/$', view = views.Acheter.acheter, name='acheter_acheter'),

    # url(r'^louer-lister$', view = views.Louer.lister, name='louer_lister'),
    # url(r'^louer/infos-supplementaire/$', view = views.Louer.infos_supplementaire, name='louer_infos_supplementaire'),
    # url(r'^louer/louer/$', view = views.Louer.louer, name='louer_louer'),

    # url(r'^vendre/$', view = views.Vendre.vendre, name='vendre_vendre'),

    url(r'^Maison$|^Maison/lister$', view = views.Maison.lister, name='lister_maison'),
    url(r'^Maison/acheter/(?P<id_maison>\d+)$', view = views.Maison.acheter, name='acheter_maison'),
    url(r'^Maison/confirmer-maison/$', view = views.Maison.confirmer_achat, name='confirmer_achat_maison'),
    url(r'^Maison-a-acheter/$', view = views.Maison.a_acheter, name='maison_a_acheter'),

    url(r'^Maison/louer/lister$', view = views.Maison.louer_lister, name='louer_lister_maison'),
    url(r'^Maison/louer/(?P<id_maison>\d+)$', view = views.Maison.louer, name='louer_maison'),
    url(r'^Maison-a-louer/$', view = views.Maison.a_louer, name='maison_a_louer'),

    url(r'^Maison/vendre/$', view = views.Maison.vendre, name='vendre_maison'),

    url(r'^Terrain$|^Terrain/lister$', view = views.Terrain.lister, name='lister_terrain'),
    url(r'^Terrain/acheter/(?P<id_terrain>\d+)$', view = views.Terrain.acheter, name='acheter_terrain'),
    url(r'^Maison/confirmer-terrain/$', view = views.Terrain.confirmer_achat, name='confirmer_achat_terrain'),
    url(r'^Terrain-a-acheter/$', view = views.Terrain.a_acheter, name='terrain_a_acheter'),
    url(r'^Terrain/louer/$', view = views.Terrain.louer, name='louer_terrain'),
    url(r'^Terrain/vendre/$', view = views.Terrain.vendre, name='vendre_terrain'),

    url(r'^authentification/$', view = views.Acces.authentification, name='authentification'),
    url(r'^inscription/$', view = views.Acces.inscription, name='inscription'),
    url(r'^dashboard/$', view = views.Acces.dashboard, name='dashboard'),
    url(r'^deconnexion/$', view = views.Acces.deconnexion, name='deconnexion'),

    url(r'^$', view = views.index, name='index'),
    url(r'^Accueil/a_propos/$', view=views.a_propos, name='a_propos'),
    url(r'^Accueil/contact/$', view=views.contact, name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
