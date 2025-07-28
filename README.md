# EMR-SERVER

A robust and scalable Electronic Medical Records (EMR) API built with FastAPI and PostgreSQL, featuring automated CI/CD deployment to Amazon Lightsail.

## Architecture Overview

EMR-SERVER is a containerized application consisting of three main services orchestrated by Docker Compose:

- **Nginx** (`nginx` service): Reverse proxy server serving as the public entry point on port 80
- **FastAPI** (`web` service): High-performance Python web framework exposing EMR API endpoints
- **PostgreSQL** (`db` service): Relational database for persistent EMR data storage

## Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)**: High-performance web framework for building APIs with Python
- **[PostgreSQL](https://www.postgresql.org/)**: Powerful, open-source relational database
- **[Nginx](https://nginx.org/)**: High-performance reverse proxy and web server
- **[Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)**: Containerization and service orchestration
- **[Amazon Lightsail](https://aws.amazon.com/lightsail/)**: Cloud hosting platform
- **[GitHub Actions](https://github.com/features/actions)**: CI/CD automation and deployment pipeline

## Quick Start

### Prerequisites

- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Engine & Compose)
- Python 3.x (optional, for local development)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:Virtual-Medical-Mission/EMR-SERVER.git
   cd EMR-SERVER
   ```

2. **Create environment file:**
   Contact Devom B for the EnvShare link

3. **Start the application:**
   ```bash
   docker compose up --build -d
   ```


## CI/CD Pipeline

The project uses GitHub Actions for automated deployment to Amazon Lightsail.

### Workflow Details

- **Trigger**: Pushes to the `main` branch
- **Workflow File**: `.github/workflows/deploy.yml`
- **Target**: Ubuntu instance on Amazon Lightsail

### Deployment Process

1. **Code Checkout**: Latest code from main branch
2. **SSH Setup**: Secure connection to Lightsail instance
3. **Environment Preparation**: 
   - Install/update Docker, Docker Compose, and Git
   - Configure Docker permissions
4. **Code Synchronization**:
   - Fresh clone or update existing repository
   - Reset to latest main branch state
5. **Environment Configuration**: 
   - Dynamic `.env` file creation with GitHub secrets
6. **Docker Deployment**:
   - Clean up existing containers and images
   - Build and deploy with latest code
   - Force recreation of all services

## Deployment & Updates

### Automatic Deployment

1. **Make your changes** on a feature branch
2. **Create a pull request** to the `main` branch
3. **Merge the pull request** - this triggers automatic deployment
4. **Monitor deployment** in the GitHub Actions tab

### Manual Verification
Contact Devom B if you need help manually verifying deployment 

## Contributing

We welcome contributions! Please follow our development workflow for adding features and submitting changes.

### Adding a New Feature

1. **Create a feature branch:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-new-feature-name
   ```

2. **Develop your feature:**
   - Implement your changes
   - Follow code style guidelines
   - Write clear, descriptive commit messages

3. **Test locally:**
   ```bash
   docker compose up --build -d
   # Test your changes at localhost/docs
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add description of your contribution"
   git push origin feature/your-new-feature-name
   ```

### Pull Request Workflow

1. **Create Pull Request:**
   - Go to the GitHub repository
   - Click "Compare & pull request"
   - Set base branch to `main`
   - Set compare branch to your feature branch

2. **Fill out PR details:**
   - **Title**: Clear, descriptive title
   - **Description**: Explain what changes were made and why
   - **Reviewers**: Add appropriate reviewers

3. **Review Process:**
   - Address any feedback from reviewers
   - Ensure all checks pass
   - Request re-review if needed

4. **Merge:**
   - Once approved, merge into `main`
   - This will trigger automatic deployment to production

### Commit Message Guidelines
Due you many of you being new to the Git / GitHub process. We will have you write your Git Commits in Plain English format

## Development Commands

### Docker Commands
```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild and restart
docker compose up --build -d --force-recreate

# Clean up
docker compose down -v --remove-orphans
docker image prune -f
docker container prune -f
```

### Docker Compose Services

- **nginx**: Exposed on port 80, handles routing to FastAPI
- **web**: FastAPI application, internal port 8000
- **db**: PostgreSQL database with persistent volume

## Support & Contact

For questions, issues, or contributions:

- **Discord**: `mrgod1y`
- **Email**: `devom.b@yahoo.com`
- **Issues**: [GitHub Issues](https://github.com/Virtual-Medical-Mission/EMR-SERVER/issues)

## License

This project is part of the Virtual Medical Mission initiative. Please contact the maintainers for licensing information.

---

## 🎯 Project Status

[![Deployment Status](https://github.com/Virtual-Medical-Mission/EMR-SERVER/workflows/Deploy/badge.svg)](https://github.com/Virtual-Medical-Mission/EMR-SERVER/actions)
