package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	// English: Define a handler for the root path.
	// Français: Définit un gestionnaire pour la route racine.
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// English: Log the incoming request.
		// Français: Journalise la requête entrante.
		log.Printf("Received request from %s for %s", r.RemoteAddr, r.URL.Path)

		// English: Send a response.
		// Français: Envoie une réponse.
		fmt.Fprintln(w, "Hello from Qiria Core Server! / Bonjour depuis le Serveur Cœur Qiria !")
	})

	// English: Start the HTTP server on port 8080.
	// Français: Démarre le serveur HTTP sur le port 8080.
	log.Println("Qiria Core server starting on port 8080...")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
