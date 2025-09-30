# Guide de contribution

Merci de votre intérêt pour contribuer à **EneoNewsletter** ! 🎉

Ce document fournit des directives pour contribuer au projet de manière efficace et cohérente.

## Table des matières

- [Code de conduite](#code-de-conduite)
- [Comment contribuer](#comment-contribuer)
- [Configuration de l'environnement](#configuration-de-lenvironnement)
- [Standards de code](#standards-de-code)
- [Processus de Pull Request](#processus-de-pull-request)
- [Conventions de commit](#conventions-de-commit)
- [Signalement de bugs](#signalement-de-bugs)
- [Suggestions de fonctionnalités](#suggestions-de-fonctionnalités)

## Code de conduite

En participant à ce projet, vous acceptez de respecter notre code de conduite. Soyez respectueux, constructif et professionnel dans toutes vos interactions.

## Comment contribuer

Il existe plusieurs façons de contribuer :

1. **Signaler des bugs** : Ouvrez une issue avec une description détaillée
2. **Proposer des fonctionnalités** : Discutez de nouvelles idées via les issues
3. **Améliorer la documentation** : Corriger des fautes, clarifier des sections
4. **Soumettre du code** : Corriger des bugs ou implémenter des fonctionnalités

## Configuration de l'environnement

### 1. Fork et clone

```bash
# Fork le projet sur GitHub, puis clonez votre fork
git clone https://github.com/votre-username/EneoNewsletter.git
cd EneoNewsletter

# Ajoutez le dépôt original comme remote upstream
git remote add upstream https://github.com/Starland9/EneoNewsletter.git
```

### 2. Créer une branche

```bash
# Mettez à jour votre branche main
git checkout main
git pull upstream main

# Créez une branche pour votre contribution
git checkout -b feature/ma-fonctionnalite
# ou
git checkout -b fix/mon-correctif
```

### 3. Configuration de l'environnement

```bash
# Créez le fichier .env
cp .env.example .env

# Lancez l'application avec Docker
docker-compose up --build -d

# Appliquez les migrations
docker-compose exec web python manage.py migrate

# Créez un superutilisateur
docker-compose exec web python manage.py createsuperuser
```

## Standards de code

### Style Python

- Suivre [PEP 8](https://pep8.org/)
- Utiliser des noms de variables descriptifs en anglais ou français (cohérence)
- Documenter les fonctions complexes avec des docstrings
- Limiter les lignes à 120 caractères maximum

### Django

- Suivre les [conventions Django](https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/)
- Utiliser les class-based views quand approprié
- Organiser les imports dans l'ordre : stdlib, third-party, local
- Utiliser les traductions Django pour les textes utilisateur

### Exemple de code

```python
from django.db import models
from django.utils.translation import gettext_lazy as _


class Newsletter(models.Model):
    """Modèle représentant une newsletter."""
    
    subject = models.CharField(
        max_length=200,
        verbose_name=_("Sujet")
    )
    content = models.TextField(
        verbose_name=_("Contenu")
    )
    
    class Meta:
        verbose_name = _("Newsletter")
        verbose_name_plural = _("Newsletters")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.subject
```

## Processus de Pull Request

### Avant de soumettre

1. **Tests** : Assurez-vous que tous les tests passent
   ```bash
   docker-compose exec web python manage.py test
   ```

2. **Code style** : Vérifiez la conformité du code
   ```bash
   # Si flake8 est installé
   docker-compose exec web flake8 .
   ```

3. **Migrations** : Vérifiez qu'aucune migration n'est manquante
   ```bash
   docker-compose exec web python manage.py makemigrations --check --dry-run
   ```

### Créer la Pull Request

1. **Commit** vos changements avec des messages clairs
   ```bash
   git add .
   git commit -m "feat: ajout de la fonctionnalité X"
   ```

2. **Push** vers votre fork
   ```bash
   git push origin feature/ma-fonctionnalite
   ```

3. **Ouvrez une Pull Request** sur GitHub avec :
   - Un titre descriptif
   - Une description détaillée des changements
   - Des captures d'écran si interface utilisateur
   - La référence aux issues concernées (ex: "Fixes #123")

### Checklist PR

Avant de soumettre, vérifiez que :

- [ ] Le code suit les standards du projet
- [ ] Les tests existants passent
- [ ] De nouveaux tests sont ajoutés si nécessaire
- [ ] La documentation est mise à jour
- [ ] Les migrations sont créées si nécessaire
- [ ] Pas de conflits avec la branche main
- [ ] Les messages de commit suivent les conventions

## Conventions de commit

Nous utilisons [Conventional Commits](https://www.conventionalcommits.org/) :

### Format

```
<type>(<scope>): <description>

[corps optionnel]

[footer optionnel]
```

### Types

- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation uniquement
- `style`: Formatage, point-virgules manquants, etc.
- `refactor`: Refactorisation sans changement de fonctionnalité
- `perf`: Amélioration des performances
- `test`: Ajout ou modification de tests
- `chore`: Maintenance, dépendances, configuration

### Exemples

```bash
feat(newsletter): ajout de l'export CSV des abonnés
fix(coupure): correction du filtrage par quartier
docs(readme): mise à jour des instructions d'installation
style(admin): amélioration de l'interface d'administration
refactor(tasks): simplification de la logique d'envoi
test(newsletter): ajout des tests pour le modèle Subscriber
chore(deps): mise à jour de Django vers 5.2.1
```

### Scope (optionnel)

Le scope précise la partie du code affectée :
- `newsletter`: Application newsletter
- `coupure`: Application coupure
- `admin`: Interface d'administration
- `api`: API endpoints
- `tasks`: Tâches Celery
- `models`: Modèles Django
- `views`: Vues Django
- `templates`: Templates HTML
- `docker`: Configuration Docker
- `deps`: Dépendances

## Signalement de bugs

### Avant de signaler

1. Vérifiez que le bug n'a pas déjà été signalé
2. Assurez-vous d'utiliser la dernière version
3. Vérifiez que c'est bien un bug et non une erreur de configuration

### Template de bug report

```markdown
**Description du bug**
Description claire et concise du problème.

**Comment reproduire**
1. Aller sur '...'
2. Cliquer sur '...'
3. Faire défiler jusqu'à '...'
4. Voir l'erreur

**Comportement attendu**
Description de ce qui devrait se passer.

**Captures d'écran**
Si applicable, ajoutez des captures d'écran.

**Environnement**
- OS: [ex: Ubuntu 22.04]
- Docker version: [ex: 24.0.5]
- Python version: [ex: 3.11]
- Version du projet: [ex: commit hash ou tag]

**Logs**
```
Collez ici les logs pertinents
```

**Contexte additionnel**
Toute autre information utile.
```

## Suggestions de fonctionnalités

### Template de feature request

```markdown
**Le problème**
Description claire du problème que cette fonctionnalité résoudrait.

**Solution proposée**
Description de la solution que vous aimeriez voir.

**Alternatives considérées**
Autres solutions ou fonctionnalités que vous avez envisagées.

**Contexte additionnel**
Toute autre information ou capture d'écran.
```

## Questions ?

Si vous avez des questions, n'hésitez pas à :
- Ouvrir une issue avec le label `question`
- Contacter le mainteneur : [landrysimo99@gmail.com](mailto:landrysimo99@gmail.com)

---

Merci de contribuer à **EneoNewsletter** ! 🚀
