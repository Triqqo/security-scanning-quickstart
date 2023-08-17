# Local & CI/CD
## Static code analysis
```
snyk code test
```

## Open source libraries
```
pip install -r requirements.txt
snyk test
```

## Container scan
```
docker build -t app:latest .
snyk container test app:latest --file=Dockerfile
```

## IaC test
```
snyk iac test
```

# Monitoring
## Static code analysis 
**closed beta, doesn't work yet**
```
snyk code test --report --project-name=app
```

## Open source libraries
```
pip install -r requirements.txt
snyk monitor --project-name=demo-app --target-reference=main
```

## Container scan
```
docker build -t app:latest .
snyk container monitor --file=Dockerfile --project-name=demo-app app:latest
```
- `--project-name` doesn't affect "target" in the UI, contrary to other methods
- can't use `--target-reference=<branch_name>` here

## IaC test
```
snyk iac test --report --target-name=demo-app --target-reference=main
```
- `monitor` is `test --report` here
- `--project-name` is now `--target-name`

#