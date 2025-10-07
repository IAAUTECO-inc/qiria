# Qiria - Secure Hybrid Assistant

## 🇬🇧 English

### Project Overview

Qiria is a secure, on-premise, hybrid application designed to meet the stringent requirements of NIS2, ISO 27001, and Zero Trust architecture. It combines a high-performance backend written in Go with a flexible and accessible user-facing assistant written in Python with a Qt GUI.

The entire system is designed to be deployed and orchestrated via Kubernetes.

### Architecture

- **Backend Services (`/services/api-server`)**: Written in **Go**. Responsible for core business logic, API endpoints (REST/gRPC), database interactions, and security-critical operations.
- **Assistant Service (`/services/qiria-assistant`)**: Written in **Python**. Provides the "Super Siri" assistant functionality, the Qt graphical user interface, and integration with local AI/ML models.
- **Deployment (`/deployments`)**: Contains Kubernetes manifests (or Helm charts) for deploying all microservices, databases, and required infrastructure in a reproducible and auditable manner.
- **CI/CD (`/.github/workflows`)**: Automated workflows for building, testing, scanning (SBOM, vulnerabilities), and deploying the applications.

---

## 🇫🇷 Français

### Aperçu du Projet

Qiria est une application hybride, sécurisée et "on-premise", conçue pour répondre aux exigences strictes des normes NIS2, ISO 27001 et de l'architecture Zero Trust. Elle combine un backend haute performance écrit en Go avec un assistant utilisateur flexible et accessible écrit en Python avec une IHM en Qt.

L'ensemble du système est conçu pour être déployé et orchestré via Kubernetes.

### Architecture

- **Services Backend (`/services/api-server`)**: Écrits en **Go**. Responsables de la logique métier principale, des points d'accès API (REST/gRPC), des interactions avec la base de données et des opérations critiques pour la sécurité.
- **Service Assistant (`/services/qiria-assistant`)**: Écrit en **Python**. Fournit la fonctionnalité d'assistant "Super Siri", l'interface graphique Qt et l'intégration avec les modèles d'IA/ML locaux.
- **Déploiement (`/deployments`)**: Contient les manifestes Kubernetes (ou charts Helm) pour déployer tous les microservices, bases de données et l'infrastructure requise de manière reproductible et auditable.
- **CI/CD (`/.github/workflows`)**: Workflows automatisés pour compiler, tester, analyser (SBOM, vulnérabilités) et déployer les applications.