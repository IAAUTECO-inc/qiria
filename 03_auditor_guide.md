# Guide Auditeur

Ce guide fournit les informations nécessaires pour auditer la conformité et la sécurité du système Qiria.

## Points de Contrôle Clés

- **Journalisation (`Logging`)**: Tous les accès, décisions d'autorisation et actions critiques sont journalisés. Les journaux sont centralisés et protégés contre la modification. Le Serveur Cœur (`services/core`) est responsable de la génération de ces journaux.

- **Contrôle d'Accès (`RBAC`)**: La logique de contrôle d'accès basée sur les rôles (Admin, Utilisateur, Auditeur) est implémentée dans le module `auth` du Serveur Cœur. Chaque requête API est soumise à une vérification d'autorisation.

- **Génération SBOM**: Un Software Bill of Materials (SBOM) est généré pour chaque service lors du pipeline CI/CD, permettant une analyse complète des dépendances.

- **Séparation des Données**: L'accès à la base de données est contrôlé par le Serveur Cœur, qui applique une politique de "besoin d'en connaître" stricte. Les workers n'ont pas d'accès direct à la base de données.