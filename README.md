Set-Content -Path README.md -Value "# SecOps Multi-Threaded Port Scanner

A lightweight, high-performance multi-threaded port scanner written in Python and fully containerized with Docker. Designed for rapid infrastructure reconnaissance and security auditing.

## Features
- **Multi-threaded Architecture**: Utilizes Python concurrent futures to scan large port ranges rapidly.
- **Containerized Environment**: Packaged in a secure, minimal Docker container (\`python:3.11-slim\`) for consistent execution across any OS.
- **Configurable Parameters**: Custom port ranges, thread counts, and connection timeouts via CLI arguments.
- **Clean CLI Output**: Formatted logging for open ports and scan duration.

## Tech Stack
- **Language**: Python 3.11
- **Containerization**: Docker
- **Networking**: Socket programming, Concurrent execution

## Project Structure
\`\`\`text
secops-port-scanner/
│
├── main.py          # Core multi-threaded scanning logic & CLI arguments
├── requirements.txt # Project dependencies
└── Dockerfile       # Container definition
\`\`\`

## Quick Start (Docker)

1. **Build the Docker image**:
   \`\`\`bash
   docker build -t secops-scanner .
   \`\`\`

2. **Run the scanner against a target**:
   \`\`\`bash
   docker run --rm secops-scanner <TARGET_IP_OR_DOMAIN>
   \`\`\`

### Advanced Usage
Customize ports and threads:
\`\`\`bash
docker run --rm secops-scanner -p 1-10000 -t 200 127.0.0.1
\`\`\`
" -Encoding UTF8
