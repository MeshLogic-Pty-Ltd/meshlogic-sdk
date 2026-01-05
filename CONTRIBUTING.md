# Contributing to MeshLogic SDK

Thank you for your interest in contributing to the MeshLogic SDK!

## Development Setup

### Python

```bash
cd python
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

### Go

```bash
cd go
go mod download
go build ./...
```

### TypeScript

```bash
cd typescript
npm install
npm run build
```

## Running Tests

### Python

```bash
cd python
pytest tests/ -v
ruff check meshlogic
mypy meshlogic
```

### Go

```bash
cd go
go test ./...
go vet ./...
staticcheck ./...
```

### TypeScript

```bash
cd typescript
npm test
npm run lint
npm run typecheck
```

## Making Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests for the affected SDK(s)
5. Commit with a clear message
6. Push and create a pull request

## Pull Request Guidelines

- Keep PRs focused on a single change
- Update tests for new functionality
- Update documentation if needed
- Follow existing code style

## Releasing

Releases are automated via GitHub Actions:

- **Python**: Tag with `python-v0.1.0` format
- **Go**: Tag with `go-v0.1.0` format
- **TypeScript**: Tag with `typescript-v0.1.0` format

## Code of Conduct

Be respectful and constructive in all interactions.

## Questions?

Open an issue or email support@meshlogic.ai
