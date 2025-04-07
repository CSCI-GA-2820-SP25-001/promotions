# NYU DevOps Project Template


![Build Status](https://github.com/CSCI-GA-2820-SP25-001/promotions/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/tburke-nyu/promotions/branch/master/graph/badge.svg)](https://codecov.io/gh/tburke-nyu/promotions)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Open in Remote - Containers](https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/<your-repo>)

NYU DevOps project for managing **Promotions** in an e-commerce platform. This service provides RESTful APIs for managing discounts, special offers, and promotions.

## Overview

This is a **Promotions Service** for managing discounts in an e-commerce platform. It allows users to create, update, delete, and track various promotions such as:
- ✅ **Percentage discounts**
- ✅ **Buy-One-Get-One (BOGO) offers**
- ✅ **Flat rate discounts ($10 off, etc.)**
- 🚧 **Query filters for promotions (upcoming)**
- 🚧 **Stateful actions on promotions (upcoming)**

## Introduction
As Software Engineers, it's crucial to test and ensure code stability. You can learn more about this in the article: [A Case for Test Driven Development](https://johnrofrano.medium.com/a-case-for-test-driven-development-7d9a552e0a16)

---

## 📌 Prerequisite Software Installation

This project uses **Docker** and **Visual Studio Code with Remote Containers** for consistent development environments.

Install the following:
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Visual Studio Code](https://code.visualstudio.com)
- [Remote Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

Alternatively, use [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) for virtual environments. More info in [Creating Reproducible Development Environments](https://johnrofrano.medium.com/creating-reproducible-development-environments-fac8d6471f35).

---

## 📌 Bring up the Development Environment

### 🚀 Start Developing with Visual Studio Code and Docker

1. **Clone and navigate into the repository:**

```bash
git clone https://github.com/<your-repo>.git
cd <your-repo>
```

2. **Launch Visual Studio Code**:

```bash
code .
```

3. When prompted to **"Reopen in Container"**, select **"Yes"**.

This will build your containerized environment automatically.

---

## 📌 Running the Service

### Option 1: Run Locally (without Docker)

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Start the Flask app**:
```bash
flask run
```

The service will run at: **http://localhost:5000/**

### Option 2: Running with Docker

Use Docker Compose:

```bash
docker-compose up
```

The service will be available at **http://localhost:5000/** (unless specified otherwise).

---

## 📌 Running Tests

Run tests before any code changes to confirm all existing functionality works:

```bash
make test
```

To run linting for code quality:

```bash
make lint
```

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`    | `/promotions`         | List all promotions |
| `POST`   | `/promotions`         | Create a new promotion |
| `GET`    | `/promotions/{id}`    | Get a specific promotion |
| `PUT`    | `/promotions/{id}`    | Update a promotion |
| `DELETE` | `/promotions/{id}`    | Delete a promotion |
| 🚧 `GET`  | `/promotions?type=BOGO`| Query promotions by type (upcoming) |
| 🚧 `PUT` | `/promotions/{id}/activate` | Activate a promotion (upcoming) |

---

## 📌 Shutdown Development Environment

### Using Docker
```bash
docker-compose down
```

### Using Vagrant
```bash
exit
vagrant halt
```
To remove VM:
```bash
vagrant destroy
```

---

## 📌 What's Featured in this Project?

- `service/__init__.py` — Flask app setup
- `service/models.py` — Promotion data model
- `service/routes.py` — Flask routes for API
- `tests/` — Test suites for models and API

---

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

## License

Copyright (c) 2016, 2025 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
