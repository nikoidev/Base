# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite with pytest (86% coverage)
- CI/CD pipelines with GitHub Actions
  - Automated testing on push and PR
  - Code quality checks (Black, flake8, isort, mypy)
  - Security scanning (Bandit, Safety)
- Pre-commit hooks for local development
- Environment variable templates (.env.example)
- Dependabot configuration for automatic updates
- Coverage badges and CI status badges

### Changed
- Updated Pydantic to v2.10.0 with new configuration format
- Improved configuration with SettingsConfigDict

### Fixed
- Pydantic v2 compatibility issues in Settings class

## [2.0.0] - 2024-12-06

### Added
- Complete user management system with CRUD operations
- Role-Based Access Control (RBAC)
- JWT authentication with access tokens
- Audit logging system
- User profile management with avatars
- Search, filtering, and pagination
- Docker Compose setup for PostgreSQL and pgAdmin
- FastAPI backend with SQLAlchemy ORM
- Next.js 14 frontend with TypeScript
- Tailwind CSS for styling
- Dark/Light theme toggle

### Security
- Password hashing with bcrypt
- JWT token authentication
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy

## [1.0.0] - Initial Release

### Added
- Basic project structure
- Database schema
- Initial API endpoints
- Frontend scaffolding
