package main

import (
	"context"
	"log"
	"net"

	pb "qiria/core" // Importe le code généré par protoc

	"google.golang.org/grpc"
)

// server est utilisé pour implémenter le service QiriaCore.
type server struct {
	pb.UnimplementedQiriaCoreServer // Requis pour la compatibilité ascendante.
}

// RequestReport implémente la méthode de l'interface QiriaCoreServer.
func (s *server) RequestReport(ctx context.Context, in *pb.ReportRequest) (*pb.ReportResponse, error) {
	log.Printf("Received Report Request: ID=%v, Params=%v", in.GetReportId(), in.GetParametersJson())

	// TODO: Ici, nous enverrions la tâche à un worker (ex: via une message queue).

	// Pour l'instant, nous retournons une réponse simple.
	return &pb.ReportResponse{
		TaskId: "task-12345",
		Status: "QUEUED",
	}, nil
}

func main() {
	// Démarre un listener sur le port 50051.
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	// Crée une nouvelle instance du serveur gRPC.
	s := grpc.NewServer()
	pb.RegisterQiriaCoreServer(s, &server{})
	log.Printf("Qiria Core gRPC server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
