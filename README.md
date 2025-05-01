# P2P DHT File & Key–Value Storage

## Overview
This project implements a simple peer-to-peer DHT-based system with two services:

1. **File Storage**: Upload/download files to any node.
2. **Key–Value Store**: Store and retrieve string values by key, routed via SHA-1-based consistent hashing.

## Prerequisites
- Python 3.8+
- Docker & Docker Compose (v1.27+)
- `make` (optional)

## Getting Started

1. **Build containers**
   ```bash
   make build