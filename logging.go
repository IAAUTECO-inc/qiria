package logging

// Ce package centralisera la configuration de la journalisation.
// Il s'assurera que tous les journaux (accès, erreurs, audit) sont formatés de manière standard (ex: JSON)
// et envoyés vers la sortie appropriée (stdout pour Kubernetes, fichier, etc.).
// TODO: Implémenter un logger structuré (par ex. avec 'slog').
