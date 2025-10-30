# Changelog

All notable changes to CFWorker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite with pytest (tests/ directory)
- Test coverage reporting configuration
- pytest configuration in pyproject.toml
- py.typed marker for type hint support
- CONTRIBUTING.md with detailed contribution guidelines
- Security Best Practices section in README.md
- Known Limitations section in README.md
- Security notes in QUICKSTART.md
- Development setup instructions in README.md
- Code quality and testing documentation

### Changed
- Updated author information in pyproject.toml (Mack <mack@roamhq.io>)
- Enhanced development dependencies (pytest-cov, responses)
- Migrated to src/ layout for better package isolation
- Consolidated dependency management in pyproject.toml
- Updated requirements.txt and requirements-dev.txt to reference pyproject.toml
- Improved README.md with security warnings and best practices
- Enhanced QUICKSTART.md with security considerations
- Updated Development section with proper paths (src/cfworker/)
- Expanded Contributing section with detailed process

### Security
- Added security warnings about .env file permissions
- Documented credential protection best practices
- Added deployment safety guidelines
- Documented known security considerations

## [0.1.0] - 2024-10-30

### Added
- Initial release of CFWorker
- Python CLI tool for Cloudflare Workers deployment
- Core commands: init, deploy, delete, list, info, config-setup
- Cloudflare API client wrapper with full Workers API support
- Configuration management via .cfworker.json and .env files
- Deployment logic with validation and error handling
- Three worker templates: API, static site, and edge function
- Working examples: hello-world and kv-storage
- Comprehensive documentation (README.md and QUICKSTART.md)
- Cloudflare Workers expert agent for Claude Code
- MIT License
- Modern Python packaging with pyproject.toml
- Development tooling: black, ruff

### Features
- Deploy workers to Cloudflare in seconds
- Initialize projects from templates
- Manage environment variables and secrets
- List and inspect deployed workers
- Interactive credential setup
- Dry-run deployment validation
- Rich CLI output with colors and formatting

[Unreleased]: https://github.com/yourusername/CFWorker/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/CFWorker/releases/tag/v0.1.0
