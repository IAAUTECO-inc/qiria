# Guide Développeur

Ce document décrit l'architecture technique de Qiria et les conventions de développement.

## Architecture

Le système est basé sur une architecture microservices avec un modèle modulaire.

- **Serveur Cœur (`/services/core`)**: Écrit en Go. Point d'entrée unique, il gère l'authentification, les autorisations et la distribution des tâches.
- **Modules Workers (`/services/workers`)**: Services Python spécialisés pour le reporting, le scripting et l'audit.
- **Interface Utilisateur (`/services/ui`)**: Client lourd en Python/Qt qui communique exclusivement avec le Serveur Cœur.
- **Connecteur Grafana (`/services/grafana-connector`)**: Un plugin de source de données pour Grafana, écrit en Go. Il agit comme un client gRPC du Serveur Cœur pour afficher les données de reporting dans Grafana.

## Communication Inter-Services

La communication entre le Serveur Cœur et les Workers se fait via gRPC. Les définitions de protocole (`.proto`) sont stockées dans `/services/core/api/proto`.

Le connecteur Grafana utilise également cette même interface gRPC pour interroger le Serveur Cœur, garantissant un point d'entrée unique et une politique de sécurité cohérente.

## Connecteurs Externes

### Connecteur FreeIPA (LDAP)

Pour s'intégrer aux systèmes d'authentification d'entreprise, Qiria peut utiliser des connecteurs. Un connecteur pour **FreeIPA** est prévu pour être implémenté au sein du **Serveur Cœur**.

-   **Objectif** : Permettre aux utilisateurs de s'authentifier avec leurs identifiants FreeIPA.
-   **Fonctionnement** : Le Serveur Cœur utilisera le protocole LDAP pour communiquer avec le serveur FreeIPA.
-   **Processus** :
    1.  L'utilisateur fournit son nom d'utilisateur et son mot de passe via l'interface utilisateur.
    2.  Le Serveur Cœur effectue une opération `bind` LDAP sur le serveur FreeIPA pour valider les identifiants.
    3.  En cas de succès, il récupère les groupes de l'utilisateur dans FreeIPA.
    4.  Ces groupes sont mappés aux rôles RBAC de Qiria (`Admin`, `User`, `Auditor`).
    5.  Le Serveur Cœur génère un JWT contenant les permissions appropriées pour l'utilisateur.

## Conventions de Code

*À définir (ex: style de code, gestion des erreurs, journalisation).*