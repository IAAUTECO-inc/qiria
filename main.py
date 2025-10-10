import sys
import json
import logging
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QFormLayout,
    QMessageBox, QDialog, QDialogButtonBox
    QMessageBox, QDialog, QDialogButtonBox, QCheckBox
)
from PySide6.QtCore import Slot, QThread, Signal
from PySide6.QtCore import Slot, QThread, Signal, Qt

# Ajoute le dossier 'api/gen' au path pour trouver les modules gRPC générés
# 🇬🇧 Add the 'api/gen' directory to the path to find the generated gRPC modules
# 🇫🇷 Ajoute le dossier 'api/gen' au path pour trouver les modules gRPC générés
api_gen_path = Path(__file__).resolve().parent / 'api/gen'
if api_gen_path.exists():
    sys.path.append(str(api_gen_path))
    import qiria_pb2
    import qiria_pb2_grpc
else:
    print(f"Erreur: Le répertoire des stubs gRPC n'a pas été trouvé: {api_gen_path}")
    print("Veuillez exécuter le script 'generate.sh' à la racine du projet.")
    sys.exit(1)

import grpc

class LoginDialog(QDialog):
    """
    🇬🇧 Login dialog to obtain the authentication token.
    🇫🇷 Boîte de dialogue de connexion pour obtenir le token d'authentification.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Authentification Qiria")
        self.token = None

        layout = QVBoxLayout(self)

        # NOTE: Dans une version future, on remplacera ce champ par
        # des champs "utilisateur/mot de passe" et un appel gRPC pour
        # récupérer le token. Pour l'instant, on colle le token directement.
        # 🇬🇧 NOTE: In a future version, this field will be replaced by
        # "username/password" fields and a gRPC call to retrieve the token.
        # For now, we paste the token directly.
        # 🇫🇷 NOTE: Dans une version future, on remplacera ce champ par des champs "utilisateur/mot de passe" et un appel gRPC pour récupérer le token. Pour l'instant, on colle le token directement.
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Coller le token JWT ici")

        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Token d'authentification (JWT):"), self.token_input)
        layout.addLayout(form_layout)

        # 🇬🇧 OK and Cancel buttons
        # 🇫🇷 Boutons OK et Annuler
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self):
        """
        🇬🇧 When the user clicks OK, we check that the token is not empty.
        🇫🇷 Quand l'utilisateur clique sur OK, on vérifie que le token n'est pas vide.
        """
        if not self.token_input.text():
            QMessageBox.warning(self, "Token manquant", "Veuillez fournir un token d'authentification.")
            return
        self.token = self.token_input.text()
        super().accept()

    @staticmethod
    def get_token(parent=None):
        """
        🇬🇧 Static method to display the dialog and return the token.
        🇫🇷 Méthode statique pour afficher la dialogue et retourner le token.
        """
        dialog = LoginDialog(parent)
        if dialog.exec() == QDialog.Accepted:
            return dialog.token
        return None


class MainWindow(QMainWindow):
    """
    🇬🇧 Main window of the Qiria client application.
    🇫🇷 Fenêtre principale de l'application cliente Qiria.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qiria UI Client")
        # 🇬🇧 Token storage for the session
        # 🇫🇷 Stockage du token pour la session
        self.jwt_token = None
        self.setGeometry(100, 100, 700, 500)

        # --- Widgets ---
        self.server_address_input = QLineEdit("localhost:50051")
        self.report_id_input = QLineEdit("nis2_compliance_v1")
        self.report_params_input = QLineEdit('{"target_host": "srv-prod-db-01", "scan_profile": "full"}')
        self.request_button = QPushButton("Demander le Rapport")
        self.use_tls_checkbox = QCheckBox("Utiliser le chiffrement TLS")
        self.ca_cert_input = QLineEdit("certs/ca.pem") # 🇬🇧 Path to the CA certificate / 🇫🇷 Chemin vers le certificat CA
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        # --- Layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        form_layout = QFormLayout()
        form_layout.addRow("Adresse du Serveur gRPC:", self.server_address_input)
        form_layout.addRow("ID du Rapport:", self.report_id_input)
        form_layout.addRow("Paramètres (JSON):", self.report_params_input)
        form_layout.addRow(self.use_tls_checkbox)
        form_layout.addRow("Certificat CA (pour TLS):", self.ca_cert_input)

        layout.addLayout(form_layout)
        layout.addWidget(self.request_button)
        layout.addWidget(QLabel("Logs et Résultats:"))
        layout.addWidget(self.log_output)

        # --- Connections ---
        self.request_button.clicked.connect(self.request_report)
        self.use_tls_checkbox.stateChanged.connect(self.toggle_ca_cert_input)

        # 🇬🇧 Initial state
        # 🇫🇷 État initial
        self.use_tls_checkbox.setChecked(True)

        self.log("Client prêt. Configurez la requête et cliquez sur 'Demander le Rapport'.")

    def log(self, message: str):
        """
        🇬🇧 Displays a message in the text area.
        🇫🇷 Affiche un message dans la zone de texte.
        """
        self.log_output.append(message)
        print(message) # 🇬🇧 Also display in the console / 🇫🇷 Affiche aussi dans la console

    def set_token(self, token: str):
        """
        🇬🇧 Stores the JWT and updates the window title to show the connected state.
        🇫🇷 Stocke le token JWT et met à jour le titre de la fenêtre pour indiquer l'état connecté.
        """
        self.jwt_token = token
        self.setWindowTitle(f"Qiria UI Client (Connecté)")

    @Slot(int)
    def toggle_ca_cert_input(self, state):
        self.ca_cert_input.setEnabled(state == Qt.Checked)

    @Slot()
    def request_report(self):
        """
        🇬🇧 Connects to the gRPC server and sends a report request.
        🇫🇷 Se connecte au serveur gRPC et envoie une requête de rapport.
        """
        server_address = self.server_address_input.text()
        report_id = self.report_id_input.text()
        params_str = self.report_params_input.text()

        if not self.jwt_token:
            self.log("Erreur: Authentification requise. Aucun token n'est défini.")
            QMessageBox.critical(self, "Authentification requise", "Veuillez vous authentifier d'abord.")
            return

        self.log(f"Tentative de connexion à {server_address}...")
        self.request_button.setEnabled(False)

        try:
            channel = None
            if self.use_tls_checkbox.isChecked():
                ca_cert_path = self.ca_cert_input.text()
                if not ca_cert_path:
                    QMessageBox.warning(self, "Erreur TLS", "Le chemin vers le certificat CA est requis pour une connexion TLS.")
                    self.request_button.setEnabled(True)
                    return
                try:
                    with open(ca_cert_path, 'rb') as f:
                        root_certs = f.read()
                    credentials = grpc.ssl_channel_credentials(root_certificates=root_certs)
                    channel = grpc.secure_channel(server_address, credentials)
                    self.log("Création d'un canal gRPC sécurisé (TLS)...")
                except FileNotFoundError:
                    self.log(f"Erreur: Fichier certificat CA non trouvé à '{ca_cert_path}'.")
                    self.request_button.setEnabled(True)
                    QMessageBox.critical(self, "Erreur Fichier", f"Le fichier certificat '{ca_cert_path}' est introuvable.")
                    return
            else:
                channel = grpc.insecure_channel(server_address)
                self.log("Attention: Création d'un canal gRPC non sécurisé. Pour usage de développement uniquement.")

            with channel:
                stub = qiria_pb2_grpc.QiriaCoreStub(channel)

                # 🇬🇧 Validate and prepare parameters
                # 🇫🇷 Valide et prépare les paramètres
                try:
                    report_params = json.loads(params_str)
                except json.JSONDecodeError:
                    self.log("Erreur: Les paramètres ne sont pas un JSON valide.")
                    self.request_button.setEnabled(True)
                    QMessageBox.critical(self, "Erreur de Paramètres", "Le format des paramètres JSON est invalide.")
                    return

                # 🇬🇧 Prepare metadata for authentication
                # 🇫🇷 Préparation des métadonnées pour l'authentification
                metadata = [('authorization', f'Bearer {self.jwt_token}')]

                request = qiria_pb2.ReportRequest(
                    report_id=report_id,
                    parameters_json=json.dumps(report_params)
                )

                self.log(f"Envoi de la requête pour le rapport '{request.report_id}'...")
                # 🇬🇧 Send the request with the token in the metadata
                # 🇫🇷 Envoi de la requête avec le token dans les métadonnées
                response = stub.RequestReport(request, metadata=metadata)
                self.log(f"Réponse du serveur -> Task ID: {response.task_id}, Statut: {response.status}")

        except grpc.RpcError as e:
            self.log(f"Erreur gRPC: {e.details()} (code: {e.code().name})")
            QMessageBox.critical(self, "Erreur de Connexion", f"Impossible de se connecter au serveur gRPC.\n{e.details()}")
        except Exception as e:
            self.log(f"Une erreur inattendue est survenue: {e}")
        finally:
            self.request_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 🇬🇧 1. Display the login dialog
    # 🇫🇷 1. Afficher la dialogue de connexion
    token = LoginDialog.get_token()

    # 🇬🇧 2. If a token is obtained, launch the main window
    # 🇫🇷 2. Si un token est obtenu, lancer la fenêtre principale
    if token:
        window = MainWindow()
        window.set_token(token)
        window.show()
        sys.exit(app.exec())
    else:
        # 🇬🇧 The user cancelled the login, so we exit the application
        # 🇫🇷 L'utilisateur a annulé la connexion, on quitte l'application
        sys.exit(0)