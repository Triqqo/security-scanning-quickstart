# Open source security scanning quickstart for developers
### Goal
Get security scans running on a project quickly (ideally within a day), in a CI/CD pipeline

### Requirements
1. Open source
2. Open license (commercial use not restricted)
3. Usable in CI/CD pipelines (i.e. via a CLI or API, and in a container)

## Static code analysis
```
# do something
```

## Open source libraries
```
pip install -r requirements.txt
# do something
```

## Containers
```
docker build -t app:latest .
# do something
```

## Infrastructure as Code
Tool: Checkov
License: Apache
Repo: https://github.com/bridgecrewio/checkov/
```
# do something (checkov?)
```

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

### IaC test
```
snyk iac test --report --target-name=demo-app --target-reference=main
```
- `monitor` is `test --report` here
- `--project-name` is now `--target-name`
