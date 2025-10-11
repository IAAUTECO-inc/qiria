# Architecture de Sécurité de Qiria

Ce document fournit une analyse approfondie de l'architecture de sécurité de Qiria, en accord avec les principes Zero Trust et les exigences des normes telles que NIS2 et ISO 27001.

## 1. Modèle de Menace (Threat Model)

Le modèle de menace de Qiria est basé sur le framework STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) et prend en compte les vecteurs d'attaque suivants :

-   **Attaques externes** : Tentatives de compromission de l'API publique du Serveur Cœur.
-   **Attaques internes / Mouvement latéral** : Tentatives de communication non autorisée entre les microservices.
-   **Attaques sur la chaîne d'approvisionnement (Supply Chain)** : Injection de dépendances malveillantes.
-   **Compromission de l'environnement d'exécution** : Évasion de la sandbox par un script malveillant.
-   **Menaces internes (Insider Threats)** : Abus de privilèges par un utilisateur légitime.

## 2. Sécurité des Composants

### 2.1. Serveur Cœur (Go) - Le "Policy Enforcement Point"

-   **Authentification (AuthN)** :
    -   Implémentation de JWT avec des tokens à courte durée de vie (`access_token`) et des `refresh_token`.
    -   Utilisation d'algorithmes de signature asymétrique (ex: RS256) pour que seul le Serveur Cœur puisse générer des tokens valides.
    -   Rotation des clés de signature gérée via un secret Kubernetes.
-   **Autorisation (AuthZ)** :
    -   Contrôle d'accès basé sur les rôles (RBAC) strict appliqué à chaque requête gRPC.
    -   Définition des rôles : `Admin`, `User`, `Auditor`, avec des permissions granulaires.
    -   La logique est centralisée dans le package `auth` pour garantir une application cohérente.
-   **Validation des entrées** :
    -   Toutes les données provenant des requêtes sont systématiquement validées pour prévenir les injections (SQLi, etc.), même si le Serveur Cœur n'interagit pas directement avec la base de données.
-   **Délégation Sécurisée à l'Orchestrateur** :
    -   Le Serveur Cœur communique avec l'API de Kestra via mTLS.
    -   Il utilise un token d'API à privilège minimum pour déclencher uniquement les workflows autorisés.

### 2.2. Communication Inter-Services

-   **TLS Mutuel (mTLS)** : Toute communication gRPC (Clients -> Serveur Cœur) et REST (Serveur Cœur -> Kestra) est chiffrée et authentifiée mutuellement via mTLS.
-   **Politiques Réseau (Kubernetes Network Policies)** : Des politiques réseau strictes isolent les services. Par exemple, un `reporting-worker` ne peut communiquer qu'avec le Serveur Cœur et non avec un `scripting-worker`.

### 2.3. Workers (Python) - Isolation et Privilège Minimum

-   **Principe du privilège minimum** : Les workers n'ont pas d'accès direct à la base de données ni à d'autres services. Ils ne font que traiter les tâches reçues du Serveur Cœur.
-   **Environnement d'exécution sécurisé (`scripting-worker`)** :
    -   **Objectif** : Exécuter des scripts Python fournis par les utilisateurs sans compromettre le système hôte.
    -   **Stratégie** : Utilisation de conteneurs "sandbox" éphémères. Chaque script est exécuté dans un conteneur Docker minimaliste (ex: basé sur `gVisor` ou avec des profils `seccomp` et `AppArmor` très stricts) qui est créé à la volée et détruit après l'exécution.
    -   **Isolation réseau** : Le conteneur sandbox n'a aucun accès réseau, sauf potentiellement à des services explicitement autorisés via un proxy contrôlé.

## 3. Sécurité des Données

-   **Chiffrement en transit** : TLS/mTLS pour toutes les communications réseau.
-   **Chiffrement au repos** : Les données sensibles dans la base de données (ex: secrets, PII) sont chiffrées au niveau applicatif avant d'être stockées.

## 4. Sécurité de la Chaîne d'Approvisionnement (CI/CD)

-   **Génération de SBOM** : Un Software Bill of Materials (SBOM) au format CycloneDX est généré pour chaque build de chaque service.
-   **Analyse de vulnérabilités** : Les images de conteneurs et les dépendances sont scannées avec des outils comme `Trivy` ou `Grype` à chaque build.
-   **Analyse statique (SAST)** : Des outils comme `gosec` (pour Go) et `bandit` (pour Python) sont intégrés au pipeline pour détecter les failles de sécurité dans le code source.
-   **Hardening des images** : Utilisation d'images de conteneurs "distroless" ou minimalistes et exécution des processus en tant qu'utilisateur non-root.

## 5. Journalisation et Audit

-   **Journalisation structurée** : Tous les services génèrent des logs au format JSON.
-   **Objectif de journalisation structurée** : Il est prévu que tous les services génèrent des logs au format JSON pour faciliter l'analyse et la corrélation.
-   **Piste d'audit immuable** : Les événements de sécurité critiques (authentification réussie/échouée, accès aux ressources, actions d'administration) sont journalisés.
-   **Centralisation** : Les logs sont collectés par l'orchestrateur (Kubernetes) et transférés vers un système de gestion de logs sécurisé (SIEM) où ils sont protégés contre toute modification.