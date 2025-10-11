<!--
[EN] The English version is an unofficial translation. In case of discrepancy, the French version prevails.
[FR] La version anglaise est une traduction non officielle. En cas de divergence, la version française prévaut.
-->

# 🇬🇧 Developer Guide / 🇫🇷 Guide Développeur

Ce document décrit l'architecture technique de Qiria et les conventions de développement.

## Architecture

Le système est basé sur une architecture microservices avec un modèle modulaire.

- **Serveur Cœur (`/services/core`)**: Écrit en Go. Point d'entrée unique, il gère l'authentification, les autorisations et la distribution des tâches.
- **Modules Workers (`/services/workers`)**: Services Python spécialisés pour le reporting, le scripting et l'audit.
- **Orchestrateur de Tâches (`Kestra`)**: Kestra est utilisé pour orchestrer l'exécution des workers. Le Serveur Cœur délègue les tâches à Kestra via son API.
- **Interface Utilisateur (`/services/ui`)**: Client lourd en Python/Qt qui communique exclusivement avec le Serveur Cœur.
- **Connecteur Grafana (`/services/grafana-connector`)**: Un plugin de source de données pour Grafana, écrit en Go. Il agit comme un client gRPC du Serveur Cœur pour afficher les données de reporting dans Grafana.

## Communication Inter-Services

---

This document describes the technical architecture of Qiria and the development conventions.

## Architecture

The system is based on a microservices architecture with a modular model.

- **Core Server (`/services/core`)**: Written in Go. Single entry point, it handles authentication, authorization, and task distribution.
- **Worker Modules (`/services/workers`)**: Specialized Python services for reporting, scripting, and auditing.
- **Task Orchestrator (`Kestra`)**: Kestra is used to orchestrate the execution of workers. The Core Server delegates tasks to Kestra via its API.
- **User Interface (`/services/ui`)**: A rich client in Python/Qt that communicates exclusively with the Core Server.
- **Grafana Connector (`/services/grafana-connector`)**: A Grafana data source plugin, written in Go. It acts as a gRPC client to the Qiria Core Server to display reporting data in Grafana.

## Inter-Service Communication

The primary communication pattern is as follows:
1.  **Clients (UI, Grafana) -> Core Server**: Secure communication via gRPC.
2.  **Core Server -> Kestra**: The Core Server calls the Kestra API (REST) to trigger a workflow execution. This communication must be secured with TLS and authentication tokens.
3.  **Kestra -> Workers**: Kestra orchestrates the workers by running them as Kubernetes Jobs. Parameters are passed securely via environment variables or configuration files.

The gRPC interface (`.proto` files) remains crucial for client-facing interactions with the Core Server.

## External Connectors

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

### FreeIPA Connector (LDAP)

To integrate with corporate authentication systems, Qiria can use connectors. A connector for **FreeIPA** is planned to be implemented within the **Core Server**.

-   **Objective**: Allow users to authenticate with their FreeIPA credentials.
-   **Operation**: The Core Server will use the LDAP protocol to communicate with the FreeIPA server.
-   **Process**:
    1.  The user provides their username and password via the user interface.
    2.  The Core Server performs an LDAP `bind` operation on the FreeIPA server to validate the credentials.
    3.  If successful, it retrieves the user's groups from FreeIPA.
    4.  These groups are mapped to Qiria's RBAC roles (`Admin`, `User`, `Auditor`).
    5.  The Core Server generates a JWT containing the appropriate permissions for the user.

## Code Conventions

*To be defined (e.g., code style, error handling, logging).*