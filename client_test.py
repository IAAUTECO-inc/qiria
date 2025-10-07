import grpc
import json
import logging
import sys
from pathlib import Path

# Ajoute le dossier 'api/gen' au path pour trouver les modules gRPC générés
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

    logging.info("Connecting to gRPC server at localhost:50051...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = qiria_pb2_grpc.QiriaCoreStub(channel)

        # Create a sample request.
        report_params = {
            "target_host": "srv-prod-db-01",
            "scan_profile": "full"
        }

        request = qiria_pb2.ReportRequest(
            report_id="nis2_compliance_v1",
            parameters_json=json.dumps(report_params)
        )

        logging.info(f"Sending request for report '{request.report_id}'...")
        response = stub.RequestReport(request)
        logging.info(f"Server responded with Task ID: {response.task_id} and Status: {response.status}")

if __name__ == '__main__':
    run()