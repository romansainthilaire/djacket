# 🧥 Djacket

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Vue.js](https://img.shields.io/badge/vue.js-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-5469d4?style=for-the-badge&logo=stripe&logoColor=ffffff)

Djacket est une application e-commerce spécialisée dans la vente de vestes.  
Le projet propose une interface moderne et une API robuste pour gérer les produits, les commandes et les paiements en ligne.

## Fonctionnalités

- Catalogue de vestes
- Recherche et filtrage de produits
- Gestion du panier
- Authentification des utilisateurs
- Paiement sécurisé avec Stripe
- Génération de factures

## Installation

### Backend (Django + DRF)

```bash
cd djacket_api
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux / macOS
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend (Vue 3)

```bash
cd djacket
npm install
npm run dev
```
