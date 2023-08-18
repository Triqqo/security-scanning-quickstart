# Open source security scanning quickstart for developers
### Goal
Get security scans running on a project quickly (ideally within a day), in a CI/CD pipeline

### Requirements
1. Open source
2. Open license (commercial use not restricted)
3. No upselling for basic features (for example, no paid upgrade required to cover all scans in a category)
4. Usable in CI/CD pipelines (i.e. via a CLI or API, and in a container)
5. Should exit > 0 if issues are found (ideally with configurable severity)

## Static code analysis
```
semgrep scan --config auto --exclude venv --error
# or from a container
docker run --rm -v "${PWD}:/src" returntocorp/semgrep semgrep scan --config auto --exclude venv --error
```

TODO: Find something that actually works. Try Semgrep https://github.com/returntocorp/semgrep

## Open source libraries
https://github.com/AppThreat/dep-scan
```
docker run --rm -v $PWD:/app ghcr.io/appthreat/dep-scan --src /app --reports-dir /app/reports
```

TODO: Check others (maybe not a reputable source). Try Trivy: https://github.com/aquasecurity/trivy

## Containers
```
docker build -t app:latest .
# do something
```
- Checkov (see below) could have also been used, but requires a paid upgrade for anything beyond basic linting of the Dockerfile (i.e. container runtime scanning, base image vulnerabilities, etc.)

TODO: Check Trivy: https://github.com/aquasecurity/trivy

## Infrastructure as Code
Tool: Checkov
License: Apache
Repo: https://github.com/bridgecrewio/checkov/
```
pip install checkov
checkov -f cloudformation.yaml --quiet
# or to run all detected scans on the entire directory (including Dockerfile):
checkov -d . --skip-path venv --quiet
```
- Note that `--quiet` only shows failed checks in the log
- Use `--hard-fail-on SEVERITY` to only fail on that severity or higher (normally fails on all issues)
- To display severity in the output, you need an API key for some reason...

## All-In-One
Tool: ShiftLeft Scan
License: MIT
Repo: https://github.com/ShiftLeftSecurity/sast-scan
```
❯ docker run --rm -e "WORKSPACE=${PWD}" -v $PWD:/app shiftleft/scan scan --build --type dockerfile,aws,python,depscan,credscan
```
- Doesn't handle static code analysis very well (misses sys.argv injection in app.py)
- Can also scan Docker images, but the report is borked. Needs either an exposed Docker socket or tarfile of the image (see readme in repo).
- Uses several other tools as scanning engines (such as Checkov) based on which files it detects

# Snyk alternative
(Used for inspiration)
## Local & CI/CD
### Static code analysis
```
snyk code test
```

### Open source libraries
```
pip install -r requirements.txt
snyk test
```

### Container scan
```
docker build -t app:latest .
snyk container test app:latest --file=Dockerfile
```

### IaC test
```
snyk iac test
```

## Monitoring
### Static code analysis 
**closed beta, doesn't work yet**
```
snyk code test --report --project-name=app
```

### Open source libraries
```
pip install -r requirements.txt
snyk monitor --project-name=demo-app --target-reference=main
```

### Container scan
```
docker build -t app:latest .
snyk container monitor --file=Dockerfile --project-name=demo-app app:latest
```
- `--project-name` doesn't affect "target" in the UI, contrary to other methods
- can't use `--target-reference=<branch_name>` here
- Note that this also scans dependencies via the app's requirements.txt (same scan as the previous one)

### IaC test
```
snyk iac test --report --target-name=demo-app --target-reference=main
```
- `monitor` is `test --report` here
- `--project-name` is now `--target-name`
