from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('admin/', index_back_office, name="indexRoot"),
    path('connexion/', connexion, name="connexion"),
    path('creation-utilisateur', creation_utilisateur, name="creation"),
    path('deconxion/', deconnexion, name="deconnexion"),
    path('admin/approuve/<str:uri>/<str:raison>/<slug:slug>/', approuve_un_domaine, name="approuve_un_domaine"),
    path('admin/blaklist/<str:uri>/<str:raison>/<slug:slug>/', black_lister_un_domaine, name="black_lister_un_domaine"),
    path('admin/domaine-blacklister/', domaine_blacklister, name='domaine_blacklister'),
    path('admin/domaine-approuver/', domainer_approuver, name='domaine_approuver'),
    path('admin/gestion-utilisateur/', gestion_utilisateur, name="gestion_utilisateur"),
    path('admin/modification/<int:id>/', modifier_utilisateur, name="modification_utilisateur"),
    path('admin/suppression/<int:id>/', supprimer_utilisateur, name="supprimer_utilisateur")
]
