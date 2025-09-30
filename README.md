# programmation_avancee

## TD1

Sur le TD1 j'ai appris a utiliser Django. Que sa soit pour __créer un projet__ puis y __ajouter une application__. J'ai aussi appris à __ajouter une url__ dans une application, __avec ou sans des paramètres__

## TP1

J'ai __créer un modèle relié à une base de données__ avec 4 entitées (Produit, Rayon, Categorie, Status) et une association (Contenir) avec une __relation many to many__. Il est possible de voir les produits, catégories et status contenus dans la base de donnée avec les chemins /monApp/produits /monApp/categories /monApp/status.

## TD2

J'ai __ajouté un administrateur__ avec la commande (python manage.py createsuperuser) et j'ai pu voir comment __afficher la page administrateur__ et la modifier avec le fichier admin.py. J'ai modifier la page admin des produits pour __modifier plusieurs produits__ en même temps. J'ai ajouté une __barre de recherche__ et __modifier les actions__ lors d'une mise a jour. J'ai ajouté une autre __colonne personnalisée__. Pour finir, j'ai ajouté une __barre de debugage__.

## TP2

Utilisation du __paramètre "request"__ pour récupérer le GET et __création d'un template__ dans le dossier templates/[nom application]/[nom fichier]. Ajout d'instructions logiques (for, if, ...) dans le template. J'ai ajouté un base.html pour le contenu global de l'application et transformé les autres pages en bloc qui extends "monApp/base.html". Ajout d'un style avec du css dans le dossier 'static' et la balise {% load static %}. __Ajout de bootstrap__ avec "django_bootstrap5".

## TD3
Modification des vues pour avoir des vues génériques en utilisant __TemplateView__, __ListView__ et __DetailView__. Ajout d'un firmulaire pour se connecter et pour creer un compte ainsi qu'un bouton pour se déconnecter. Ajout d'un formulaire dans __form.py__ pour un envoie d'email.

## TP3
Ajout de page pour l'ajout, la modification et la suppréssion d'objet.

## TD4
Affichage des pages de détails en ajoutant les informations sur leurs relations