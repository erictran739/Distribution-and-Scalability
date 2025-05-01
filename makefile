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
