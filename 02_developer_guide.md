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

## Conventions de Code

*À définir (ex: style de code, gestion des erreurs, journalisation).*