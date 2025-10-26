import grpc
import json
import logging
import sys
from pathlib import Path

# 🇬🇧 Add the 'api/gen' directory to the path to find the generated gRPC modules
# 🇫🇷 Ajoute le dossier 'api/gen' au path pour trouver les modules gRPC générés
api_gen_path = Path(__file__).resolve().parent / 'api/gen'
sys.path.append(str(api_gen_path))

import qiria_pb2
import qiria_pb2_grpc

def run():
    """
    🇬🇧 Connects to the Go gRPC server and sends a sample ReportRequest.
    🇫🇷 Se connecte au serveur gRPC Go et envoie une requête d'exemple ReportRequest.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 🇬🇧 This is a placeholder token. In a real test, this should be obtained from an auth service.
    # 🇫🇷 Ceci est un token de remplacement. Dans un test réel, il devrait être obtenu d'un service d'authentification.
    JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlRlc3QgVXNlciIsImlhdCI6MTUxNjIzOTAyMn0.dummy_signature"

    server_address = 'localhost:50051'
    ca_cert_path = 'certs/ca.pem'

    logging.info(f"🇬🇧 Attempting to connect to gRPC server at {server_address} using TLS... / 🇫🇷 Tentative de connexion au serveur gRPC à {server_address} avec TLS...")

    try:
        # 🇬🇧 Create a secure channel with TLS, using the CA certificate.
        # 🇫🇷 Créer un canal sécurisé avec TLS, en utilisant le certificat de la CA.
        with open(ca_cert_path, 'rb') as f:
            root_certs = f.read()
        credentials = grpc.ssl_channel_credentials(root_certificates=root_certs)
        channel = grpc.secure_channel(server_address, credentials)

        stub = qiria_pb2_grpc.QiriaCoreStub(channel)

        report_params = {
            "target_host": "srv-prod-db-01",
            "scan_profile": "full"
        }
        request = qiria_pb2.ReportRequest(
            report_id="nis2_compliance_v1",
            parameters_json=json.dumps(report_params)
        )

        # 🇬🇧 Prepare metadata for authentication.
        # 🇫🇷 Préparer les métadonnées pour l'authentification.
        metadata = [('authorization', f'Bearer {JWT_TOKEN}')]

        logging.info(f"🇬🇧 Sending request for report '{request.report_id}'... / 🇫🇷 Envoi de la requête pour le rapport '{request.report_id}'...")
        response = stub.RequestReport(request, metadata=metadata)
        logging.info(f"🇬🇧 Server responded with Task ID: {response.task_id} and Status: {response.status} / 🇫🇷 Réponse du serveur - Task ID: {response.task_id}, Statut: {response.status}")

    except FileNotFoundError:
        logging.error(f"🇬🇧 CA certificate file not found at '{ca_cert_path}'. / 🇫🇷 Fichier du certificat CA non trouvé à '{ca_cert_path}'.")
    except grpc.RpcError as e:
        logging.error(f"🇬🇧 gRPC error: {e.details()} (code: {e.code().name}) / 🇫🇷 Erreur gRPC: {e.details()} (code: {e.code().name})")

if __name__ == '__main__':
    run()