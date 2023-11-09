from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core import utils
from core.forms import DomaineForm
from core.models import User, DnsReclamation, Blacklist, ApprouvedDomaine


def index(request):
    if request.method == 'POST':
        uri = request.POST.get('uri')
        raison = request.POST.get('raison')
        retour = utils.verification(uri)
        if retour:
            requet = DnsReclamation.objects.create(uri=uri, raison=raison)
            done = "Votre requete a ete enregistre avec succes"
        else:
            err = "Le domaine doit etre .sn ou l'addresse Ip n'est pas valide"
        form = DomaineForm()
    else:
        form = DomaineForm()
    return render(request, 'core/index.html', locals())


@login_required
def index_back_office(request):
    domaines = DnsReclamation.objects.filter(traiter=False)
    return render(request, 'core/index_admin.html', locals())


@login_required
def black_lister_un_domaine(request, uri, raison, slug):
    domaines = DnsReclamation.objects.filter(traiter=False)
    ap_domaine = ApprouvedDomaine.objects.filter(slug=slug)
    if ap_domaine:
        err = "Le domaine a ete deja approuve"
    else:
        Blacklist.objects.create(uri=uri, raison=raison, blacklist=True, slug=slug)
        modif = DnsReclamation.objects.get(slug=slug)
        modif.traiter = not modif.traiter
        DnsReclamation.save(modif)
        done = "Le domaine a ete blacklister avec succes"
    return render(request, 'core/index_admin.html', locals())


@login_required
def approuve_un_domaine(request, uri, raison, slug):
    domaines = DnsReclamation.objects.filter(traiter=False)
    black_domaine = Blacklist.objects.filter(slug=slug)
    if black_domaine:
        err = "Le domaine a ete deja blacklister"
    else:
        ApprouvedDomaine.objects.create(uri=uri, raison=raison, appouved=True, slug=slug)
        modif = DnsReclamation.objects.get(slug=slug)
        modif.traiter = not modif.traiter
        DnsReclamation.save(modif)
        done = "Le domaine a ete approuve avec succes"
    return render(request, 'core/index_admin.html', locals())


def connexion(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            if user.is_active or user.is_staff:
                return redirect("indexRoot")
        else:
            err = "ERR lors de la connexion"
    return render(request, 'core/connexion.html', locals())


@login_required
def creation_utilisateur(request):
    if request.method == 'POST':
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_exist = User.objects.filter(email=email)
        if user_exist:
            err = "L'utilisateur existe deja !"
        else:
            user = User.objects.create_user(
                first_name=prenom,
                last_name=nom,
                email=email,
                password=password
            )
            if user:
                done = "L'utilisateur a ete cree avec succes"
    return render(request, 'core/creation_utilisateur.html', locals())


@login_required
def deconnexion(request):
    logout(request)
    return redirect("/connexion")


@login_required
def domainer_approuver(request):
    domaines = ApprouvedDomaine.objects.all()
    return render(request, 'core/appouve_domaine.html', locals())


@login_required
def domaine_blacklister(request):
    domaines = Blacklist.objects.all()
    return render(request, 'core/blacklist_domaine.html', locals())


@login_required
def gestion_utilisateur(request):
    users = User.objects.all()
    return render(request, 'core/gestion_utilisateur.html', locals())


@login_required
def modifier_utilisateur(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        user.email = email
        user.first_name = prenom
        user.last_name = nom
        user.save()
    return render(request, 'core/modification_utilisateur.html', locals())


@login_required
def supprimer_utilisateur(request, id):
    user = User.objects.get(id=id)
    user.delete()
    users = User.objects.all()
    done_sup = "Element supprimer avec succes"
    return render(request, 'core/gestion_utilisateur.html', locals())