# Ops API — AWS Docker CI/CD Pipeline

A production-style DevOps project demonstrating how to containerize a Python API, provision AWS infrastructure with Terraform, publish Docker images to Docker Hub, and automatically deploy application updates to an EC2 server using GitHub Actions.

The application code is intentionally simple so the focus remains on **infrastructure, containerization, networking, and CI/CD**.

## Overview

The project automates the journey from a code change to a running application on AWS.

```text
Developer
    │
    │ git push
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Test
    ├── Build Docker image
    └── Push image
            │
            ▼
       Docker Hub
            │
            │ pull
            ▼
       AWS EC2
            │
            ▼
     Docker Container
            │
            ▼
         Ops API
```

Infrastructure is managed separately with Terraform:

```text
Terraform
    │
    ├── VPC
    ├── Public Subnet
    ├── Internet Gateway
    ├── Route Table
    ├── Security Group
    └── EC2 Instance
```

**Terraform manages infrastructure. GitHub Actions manages application deployment.**

## Technology Stack

| Technology     | Purpose                |
| -------------- | ---------------------- |
| Python         | API application        |
| Docker         | Containerization       |
| Docker Hub     | Container registry     |
| AWS EC2        | Application server     |
| AWS VPC        | Network infrastructure |
| Terraform      | Infrastructure as Code |
| GitHub Actions | CI/CD                  |
| SSH            | Server access          |

## Application

The API is a lightweight Python HTTP server with two endpoints:

```text
GET /health
GET /system
```

Health check:

```json
{"status": "ok"}
```

The application listens on port `8000` inside the container.

On EC2, traffic is mapped from port `80` to the container:

```text
Internet
   │
   ▼
EC2 :80
   │
   ▼
Docker :8000
   │
   ▼
Ops API
```

## Docker

Build locally:

```bash
docker build -t ops-api .
```

Run:

```bash
docker run -d \
  --name ops-api \
  -p 8000:8000 \
  ops-api
```

Test:

```bash
curl http://localhost:8000/health
```

The image is published to Docker Hub as:

```text
thesportysofia/ops-api
```

The CI pipeline explicitly builds for `linux/amd64` because the AWS EC2 instance uses an x86_64 architecture.

## AWS Infrastructure

Terraform provisions the application environment in `eu-west-1`.

```text
VPC:             10.0.0.0/16
Public Subnet:   10.0.1.0/24
EC2:             t3.micro
OS:              Ubuntu 24.04
```

The EC2 instance is placed in a public subnet with internet connectivity through an Internet Gateway.

Docker is installed automatically during instance creation using EC2 `user_data`.

### Terraform

```bash
cd infra

terraform init
terraform validate
terraform plan
terraform apply
```

Terraform Registry modules are used for the VPC and EC2 resources rather than defining every underlying AWS resource manually.

## CI/CD

The GitHub Actions workflow is located at:

```text
.github/workflows/deploy.yml
```

A push to `main` triggers:

```text
GitHub
   ↓
Test application
   ↓
Build linux/amd64 image
   ↓
Push to Docker Hub
   ↓
SSH into EC2
   ↓
Pull image
   ↓
Replace running container
   ↓
Health check
```

Docker images are tagged with the Git commit SHA so each deployment can be tied to a specific version of the source code.

## Security

Sensitive values are stored as GitHub Actions secrets and are not committed to the repository.

The project also excludes Terraform state, environment files, SSH keys, and other sensitive or unnecessary files through `.gitignore` and `.dockerignore`.

SSH is currently exposed for the learning environment; a production deployment would use tighter network restrictions and stronger access controls.

## Project Structure

```text
ops-api/
├── app.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
├── .github/
│   └── workflows/
│       └── deploy.yml
└── infra/
    ├── main.tf
    ├── variables.tf
    ├── versions.tf
    ├── outputs.tf
    └── ec2.tf
```

## What This Project Demonstrates

* Docker containerization
* AWS networking
* EC2 provisioning
* Infrastructure as Code with Terraform
* Terraform Registry modules
* Docker image management
* GitHub Actions CI/CD
* Automated SSH deployment
* Deployment health checks
* Reproducible infrastructure and application delivery

## Future Improvements

* Automated application tests
* Image vulnerability scanning
* HTTPS and a domain
* Restricted SSH access
* Remote Terraform state
* Monitoring and logging
* Automatic rollback
* Staging environment

---

