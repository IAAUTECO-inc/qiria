# Guide Développeur

Ce document décrit l'architecture technique de Qiria et les conventions de développement.

## Architecture

Le système est basé sur une architecture microservices avec un modèle modulaire.

- **Serveur Cœur (`/services/core`)**: Écrit en Go. Point d'entrée unique, il gère l'authentification, les autorisations et la distribution des tâches.
- **Modules Workers (`/services/workers`)**: Services Python spécialisés pour le reporting, le scripting et l'audit.
- **Interface Utilisateur (`/services/ui`)**: Client lourd en Python/Qt qui communique exclusivement avec le Serveur Cœur.

## Communication Inter-Services

La communication entre le Serveur Cœur et les Workers se fait via gRPC. Les définitions de protocole (`.proto`) sont stockées dans `/services/core/api/proto`.

## Conventions de Code

*À définir (ex: style de code, gestion des erreurs, journalisation).*