# P2P DHT File & Key–Value Storage

## Requirements
- Python 3.8+
- Docker & Docker Compose
- GNU Make (or Git Bash on Windows)

## Quick Start
1. **Build & launch**
   ```bash
   make build && make up
   ```
2. **Verify nodes**
   ```bash
   make health
   ```

## File Storage
- **Upload** a test file:
  ```bash
  curl -F "file=@test.txt" http://localhost:5001/upload
  ```
- **Download**:
  ```bash
  curl http://localhost:5001/download/test.txt
  ```

## Key–Value Store
- **Store**:
  ```bash
  curl -X POST http://localhost:5002/kv \
    -H 'Content-Type: application/json' \
    -d '{"key":"example","value":"data"}'
  ```
- **Retrieve**:
  ```bash
  curl http://localhost:5003/kv/example
  ```



> *Curl was a little weird for me, but I changed the prefix cURL commands with `curl.exe --%` for a fix.*
