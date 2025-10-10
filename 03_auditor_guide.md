<!--
[EN] The English version is an unofficial translation. In case of discrepancy, the French version prevails.
[FR] La version anglaise est une traduction non officielle. En cas de divergence, la version française prévaut.
-->

# 🇬🇧 Auditor Guide / 🇫🇷 Guide Auditeur

Ce guide fournit les informations nécessaires pour auditer la conformité et la sécurité du système Qiria.

## Points de Contrôle Clés

- **Journalisation (`Logging`)**: Tous les accès, décisions d'autorisation et actions critiques sont journalisés. Les journaux sont centralisés et protégés contre la modification. Le Serveur Cœur (`services/core`) est responsable de la génération de ces journaux.

- **Contrôle d'Accès (`RBAC`)**: La logique de contrôle d'accès basée sur les rôles (Admin, Utilisateur, Auditeur) est implémentée dans le module `auth` du Serveur Cœur. Chaque requête API est soumise à une vérification d'autorisation.

- **Génération SBOM**: Un Software Bill of Materials (SBOM) est généré pour chaque service lors du pipeline CI/CD, permettant une analyse complète des dépendances.

- **Séparation des Données**: L'accès à la base de données est contrôlé par le Serveur Cœur, qui applique une politique de "besoin d'en connaître" stricte. Les workers n'ont pas d'accès direct à la base de données.

---

This guide provides the necessary information to audit the compliance and security of the Qiria system.

## Key Control Points

- **Logging**: All access, authorization decisions, and critical actions are logged. Logs are centralized and protected against modification. The Core Server (`services/core`) is responsible for generating these logs.

- **Access Control (`RBAC`)**: The role-based access control logic (Admin, User, Auditor) is implemented in the `auth` module of the Core Server. Each API request is subject to an authorization check.

- **SBOM Generation**: A Software Bill of Materials (SBOM) is generated for each service during the CI/CD pipeline, allowing for a complete analysis of dependencies.

- **Data Segregation**: Database access is controlled by the Core Server, which enforces a strict "need-to-know" policy. Workers do not have direct access to the database.