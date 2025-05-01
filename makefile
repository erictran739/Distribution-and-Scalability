.PHONY: build up down logs test health

build:
	docker-compose build

up:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f

# Check health endpoint on each node
health:
	@echo "Node1:" && curl -s http://localhost:5001/health || echo "Failed"
	@echo "Node2:" && curl -s http://localhost:5002/health || echo "Failed"
	@echo "Node3:" && curl -s http://localhost:5003/health || echo "Failed"

# Automated integration tests (Unix/macOS)
test: health
	@echo "Generating test.txt for upload"
	@echo "This is a test file." > test.txt
	@echo "=== Phase 1: File Upload & Download ==="
	curl -s -w "%{http_code}" -F "file=@test.txt" http://localhost:5001/upload || exit 1
	curl -s http://localhost:5001/download/test.txt > /dev/null || exit 1
	@echo "phase1 OK"

	@echo "=== Phase 2: KV Store (Local) ==="
	curl -s -X POST http://localhost:5001/kv -H "Content-Type: application/json" -d '{"key":"k1","value":"v1"}' > /dev/null || exit 1
	curl -s http://localhost:5001/kv/k1 | grep v1 || exit 1
	@echo "phase2 OK"

	@echo "=== Phase 3: DHT Routing ==="
	curl -s -X POST http://localhost:5002/kv -H "Content-Type: application/json" -d '{"key":"foo","value":"bar"}' > /dev/null || exit 1
	curl -s http://localhost:5003/kv/foo | grep bar || exit 1
	@echo "phase3 OK"