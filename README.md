# Football Calendar

This project is a scraper that fetches football matches from a website and stores them to Google Calendar. It is built using Python and the Google Calendar API and is intended to be run as a scheduled job to keep the calendar up-to-date with the latest matches every day.

## Table of Contents

- [Football Calendar](#football-calendar)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
    - [Cloning the Repository](#cloning-the-repository)
    - [Environment Variables](#environment-variables)
    - [Local Development](#local-development)
    - [Running with Docker](#running-with-docker)
  - [Docker](#docker)
    - [Dockerfile](#dockerfile)
    - [Docker Compose](#docker-compose)
  - [GitHub Actions](#github-actions)
    - [CI/CD Pipeline](#cicd-pipeline)
  - [Secrets Configuration](#secrets-configuration)
  - [Variables Configuration](#variables-configuration)
  - [Documentation](#documentation)
  - [Source Code](#source-code)
  - [Tests](#tests)
  - [Tests](#tests-1)
---

## Project Structure

```plaintext
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── 0_bug_report.yml                # Template for reporting bugs or issues
│   │   ├── 1_feature_request.yml           # Template for requesting new features
│   │   ├── 2_improvement_request.yml       # Template for suggesting improvements
│   │   ├── 3_performance_issue.yml         # Template for reporting performance issues
│   │   ├── 4_refactor_request.yml          # Template for requesting code refactoring
│   │   ├── 5_documentation_update.yml      # Template for suggesting documentation updates
│   │   ├── 6_security_vulnerability.yml    # Template for reporting security vulnerabilities
│   │   ├── 7_tests_requests.yml            # Template for requesting new tests
│   │   ├── 8_question.yml                  # Template for asking questions
│   │   └── config.yml                      # Configuration file for issue templates
│   ├── workflows/
│   │   ├── cicd.yml                        # CI/CD pipeline configuration using GitHub Actions
│   │   └── run.yml                         # Workflow to run the project scheduled
│   ├── dependabot.yml                      # Dependabot configuration for dependency updates
│   └── release.yml                         # Automatic release generation on GitHub
├── docker/
│   ├── .env.example                        # Example environment variables file for Docker
│   ├── Dockerfile                          # Dockerfile to build the project image
│   ├── Dockerfile.local                    # Dockerfile to run the project locally
│   └── compose.yml                         # Docker Compose file to define services and networks
├── docs/
│   ├── SECRETS.md                          # Documentation about secrets needed for deployment
│   └── STYLEGUIDE.md                       # Guidelines for code style and formatting
├── src/
│   ├── main.py                             # Main script of the project
│   └── requirements.txt                    # Python dependencies file
├── .dockerignore                           # File to exclude files from Docker context
├── .editorconfig                           # Configuration for code formatting in compatible editors
├── .gitignore                              # File to exclude files and directories from version control
├── AUTHORS                                 # List of authors and contributors to the project
├── CHANGELOG.md                            # History of changes and versions of the project
├── CODE_OF_CONDUCT.md                      # Code of conduct for project contributors
├── CONTRIBUTING.md                         # Guidelines for contributing to the project
├── GOVERNANCE.md                           # Project governance model and decision-making process
├── LICENSE                                 # Information about the project's license
├── README.md                               # Main documentation of the project
├── SECURITY.md                             # Documentation about project security
└── SUPPORT.md                              # Information on how to get support for the project
```

---

## Prerequisites
Before you begin, make sure you have the following installed in your environment:

- git (obligatory)
- docker (optional, if you want to run the project with Docker)
- docker-compose (optional, if you want to run the project with Docker)
- python (optional, if you want to run the project locally)

## Usage

### Cloning the Repository

To configure a new project through this repository, follow these steps:

1. Clone the repository to your local machine.

```bash
git clone git@github.com:francisjgarcia/football-calendar.git
```

2. Navigate to the cloned repository directory.

```bash
cd football-calendar
```

3. Start working on your new project!

### Environment Variables

After cloning the repository, you can develop and test the project locally. Follow these steps:

Navigate to the `src` directory and rename the `.env.example` file to `.env`. Adjust the environment variables as needed.

```bash
# Scraping environment variables
ALLOWED_TEAMS=
ALLOWED_COMPETITIONS=
SPECIAL_COMPETITIONS=
SPECIAL_CHANNELS=

# Google Calendar environment variables
GOOGLE_TOKEN=
GOOGLE_CALENDAR_NAME=
```
### Local Development

To run the project locally, follow these steps:

1. Install the dependencies:

```bash
pip install -r src/requirements.txt
```

2. Run the main script:

```bash
python src/main.py
```

### Running with Docker

You can use Docker and Docker Compose to run the project in a container. Ensure Docker and Docker Compose are installed.

1. Navigate to the docker directory, rename the `.env.example` file to `.env`, and adjust the environment variables as needed.

```bash
# Environment variables for Docker Compose
COMPOSE_PROJECT_NAME=football-calendar
COMPOSE_FILE=compose.yml

# Network configuration
DNS1=8.8.8.8
DNS2=8.8.4.4

# General environment variables
PUID=1000
PGID=1000
TZ=Europe/Madrid
```
- **COMPOSE_PROJECT_NAME**: Name of the Docker Compose project.
- **COMPOSE_FILE**: Docker Compose configuration file.
- **DNS1**: Primary DNS server.
- **DNS2**: Secondary DNS server.
- **PUID**: User ID for the container.
- **PGID**: Group ID for the container.
- **TZ**: Timezone for the container.

2. Build and run the services with Docker Compose:

```bash
compose up -d --build
```
This will build the container image according to the Dockerfile and start the services defined in `compose.yml`.

## Docker

### Dockerfile

The `Dockerfile` in the `docker` directory is used to build the Docker image for the project. The file contains instructions to create the image, including the base image, dependencies, and commands to run the application.

The `Dockerfile.local` is used to run the project locally with Docker. This file is used to build the image and run the container locally.

### Docker Compose

The `compose.yml` file in the `docker` directory defines the services and networks for the project using Docker Compose. This file specifies the container image, environment variables, ports, and volumes needed to run the application.

## GitHub Actions

### CI/CD Pipeline

This repository includes a fully automated CI/CD pipeline using `cicd.yml` GitHub Actions. The pipeline is configured to run on each push to the main or development branches and performs the following tasks:

1. **Setup**: Generates the necessary variables for use in the subsequent tasks.
2. **Build**: Builds the Docker image and saves it locally.
3. **Test**: Runs the tests for the application.
4. **Scan**: Scans the Docker image for vulnerabilities using Trivy.
5. **Push**: Pushes the Docker image to the GitHub Container Registry.
6. **Release**: Automatically generates the changelog and creates a new release on GitHub if deploying to `main`.
7. **Merge**: Merges changes from `main` into the `development` branch if a direct push to `main` occurs.

## Secrets Configuration

To properly enable the pipeline and deployment, you need to configure the following secrets in GitHub:

- **GOOGLE_TOKEN**: Google API token to access the Google Calendar API.

More details about these secrets can be found in the [SECRETS.md](docs/SECRETS.md) file.

## Variables Configuration

To properly configure the application, you need to set the following variables in the `.env.example` file:

- **ALLOWED_TEAMS**: List of teams to allow in the calendar, separated by commas.
- **ALLOWED_COMPETITIONS**: List of competitions to allow in the calendar, separated by commas.
- **SPECIAL_COMPETITIONS**: List of special competitions to allow in the calendar, separated by commas.
- **SPECIAL_CHANNELS**: List of special channels to allow in the calendar, separated by commas
- **GOOGLE_CALENDAR_NAME**: Name of the Google Calendar to store the matches.

More details about these variables can be found in the [VARIABLES.md](docs/VARIABLES.md) file.

## Documentation

The `docs` directory contains additional documentation for the project:

**STYLEGUIDE.md**: Contains guidelines for code style and formatting, including best practices for writing clean, readable code.

## Source Code

The `src` directory contains the project's source code:

**main.py**: The main script that runs the application. This is where the project's entry point is located.

**requirements.txt**: File listing the Python dependencies needed for the project. This file is used to install the required libraries via pip.

**(another scripts)**: Other scripts that are part of the project.

## Tests

The `tests` directory contains the project's test scripts. These tests can be run using the following command:

```bash
pytest src/tests/
```

## Tests

The `tests` directory contains the project's test scripts. These tests can be run using the following command:

```bash
pytest src/tests/
```

> [!NOTE]
> Actually there are no tests but they will be added in the future.

The tests are automatically run as part of the CI/CD pipeline to ensure the project's functionality is maintained.
