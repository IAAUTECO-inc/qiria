package main

import (
	"os"

	"github.com/grafana/grafana-plugin-sdk-go/backend/datasource"
	"github.com/grafana/grafana-plugin-sdk-go/backend/log"
)

// newDatasource creates a new datasource instance.
func newDatasource() datasource.ServeOpts {
	// Creates a instance manager for your plugin. The function passed
	// into `NewInstanceManger` is called when the instance is created
	// for the first time or when a datasource configuration changed.
	im := datasource.NewInstanceManager(newDataSourceInstance)
	ds := &QiriaDatasource{
		im: im,
	}

	return datasource.ServeOpts{
		QueryDataHandler:   ds,
		CheckHealthHandler: ds,
	}
}

func main() {
	// 🇬🇧 Start listening to requests sent from Grafana. This call is blocking so
	// it won't finish until Grafana shuts down the process or the plugin is stopped.
	// 🇫🇷 Commence à écouter les requêtes envoyées par Grafana. Cet appel est bloquant.
	if err := datasource.Manage("qiria-reports-datasource", newDatasource, datasource.ManageOpts{}); err != nil {
		log.DefaultLogger.Error(err.Error())
		os.Exit(1)
	}
}

// TODO:
// 1. Implémenter la structure `QiriaDatasource` et les méthodes `QueryData` et `CheckHealth`.
// 2. Dans `QueryData`, créer un client gRPC pour se connecter au Serveur Cœur de Qiria.
// 3. Utiliser les `secureJsonData` de la configuration de la datasource dans Grafana pour stocker le token d'authentification pour Qiria.
// 4. Appeler `RequestReport` puis `GetReportResult` pour récupérer les données.
// 5. Transformer le JSON du rapport en `DataFrames` pour Grafana.
