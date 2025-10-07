# Qiria 

## 🇬🇧 English

### Project Overview

Qiria is a secure, on-premise, hybrid application designed as an **advanced reporting server** to meet the stringent requirements of NIS2, ISO 27001, and Zero Trust architecture. It combines a high-performance backend written in Go with a flexible user interface and scripting engine in Python with a Qt GUI.

The entire system is designed to be deployed and orchestrated via Kubernetes.

### Architecture (Modular Model)

- **Core Server (`/services/core`)**: Written in **Go**. Acts as the lean, secure core of the system. It handles all incoming network requests, manages authentication (token validation) and authorization, and dispatches tasks to the appropriate worker modules via gRPC or a message queue. It is the single entry point, enforcing the Zero Trust security policy.
- **Worker Modules (`/services/workers`)**: A collection of specialized services written in **Python**, each handling a specific task:
  - `reporting-worker`: Generates complex compliance and business reports.
  - `scripting-worker`: Executes dynamic automation scripts.
  - `audit-worker`: Integrates with AI/ML models for advanced data analysis and auditing.
- **User Interface (`/services/ui`)**: A **Python** application using the Qt framework. It acts as a rich client that communicates exclusively with the **Core Server**'s secure API.
- **Deployment (`/deployments`)**: Contains Kubernetes manifests (or Helm charts) for deploying all microservices, databases, and required infrastructure in a reproducible and auditable manner.
- **CI/CD (`/.github/workflows`)**: Automated workflows for building, testing, scanning (SBOM, vulnerabilities), and deploying the applications.
- **Documentation (`/docs`)**: Contains user, developer, and auditor guides.

### A Note on the Name

The project is named after Qiria, a character from Iain M. Banks' renowned "Culture" series of science fiction novels. This choice reflects the project's ambition to be an advanced, intelligent, and reliable system, much like the entities within that universe.

---

## 🇫🇷 Français

### Aperçu du projet

Qiria est une application hybride, sécurisée et "on-premise", conçue comme un **serveur de reporting évolué** pour répondre aux exigences strictes des normes NIS2, ISO 27001 et de l'architecture Zero Trust. Elle combine un backend haute performance écrit en Go avec une interface utilisateur flexible et un moteur de scripting en Python avec une IHM en Qt.

L'ensemble du système est conçu pour être déployé et orchestré via Kubernetes.

### Architecture (Modèle modulaire)

- **Serveur Cœur (`/services/core`)**: Écrit en **Go**. Agit comme le cœur système, à la fois minimaliste et sécurisé. Il gère toutes les requêtes réseau entrantes, l'authentification (validation des tokens), les autorisations, et distribue les tâches aux modules de traitement (workers) via gRPC ou une file de messages. C'est le point d'entrée unique, appliquant la politique de sécurité Zero Trust.
- **Modules Workers (`/services/workers`)**: Une collection de services spécialisés écrits en **Python**, chacun gérant une tâche spécifique :
  - `reporting-worker` : Génère les rapports complexes (conformité, métier).
  - `scripting-worker` : Exécute les scripts d'automatisation dynamiques.
  - `audit-worker` : S'intègre aux modèles d'IA/ML pour l'analyse de données et l'audit.
- **Interface Utilisateur (`/services/ui`)**: Une application **Python** utilisant le framework Qt. Elle fonctionne comme un client riche qui communique exclusivement avec l'API sécurisée du **Serveur Cœur**.
- **Déploiement (`/deployments`)**: Contient les manifestes Kubernetes (ou charts Helm) pour déployer tous les microservices, bases de données et l'infrastructure requise de manière reproductible et auditable.
- **CI/CD (`/.github/workflows`)**: Workflows automatisés pour compiler, tester, analyser (SBOM, vulnérabilités) et déployer les applications.
- **Documentation (`/docs`)**: Contient les guides utilisateur, développeur et auditeur.

### Note sur le nom

Le projet est nommé d'après Qiria, un personnage de la célèbre série de romans de science-fiction "Cycle de la Culture" de Iain M. Banks. Ce choix reflète l'ambition du projet d'être un système avancé, intelligent et fiable, à l'image des entités de cet univers.
