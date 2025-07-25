# 🛍️ leboncoincoin – Mini Boutique Django

Bienvenue sur **leboncoincoin**, une boutique en ligne simple développée avec Django.

## 🚀 Fonctionnalités principales

- Parcours produits avec filtres par catégorie
- Système de panier et de paiement fictif
- Espace utilisateur (connexion, inscription, compte)
- Dashboard admin : chiffre d’affaires, commandes validées
- Notifications à la validation d'une commande (via Django signals)
- Interface responsive & soignée
- Dockerisation prête à l'emploi

---

## ⚙️ Lancer le projet avec Docker

1. **Cloner le projet**

```bash
git clone https://github.com/ton-utilisateur/bootique.git
cd bootique
```

2. **Construire et démarrer les conteneurs**

```bash
docker-compose up --build
```

3. **Accéder à l'application**

- Application : [http://localhost:8000](http://localhost:8000)
- Compte admin par défaut :
  - **Username** : `admin`
  - **Mot de passe** : `admin123`

> ⚠️ Pense à créer un superutilisateur si nécessaire avec :  
> `docker-compose exec web python manage.py createsuperuser`

---

## ⚠️ Notes

- Le dashboard n’est accessible **qu’aux superutilisateurs**
- Le favicon est chargé depuis le dossier `static/`
- Les notifications sont visibles via une cloche dans le header
- Les signaux Django sont utilisés pour déclencher des actions à la validation des commandes


---

## 👨‍💻 Auteur


Projet réalisé dans le cadre d’un apprentissage avancé de Django.
