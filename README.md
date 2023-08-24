# Open source security scanning quickstart for developers
### Goal
Get security scans running on a project quickly (ideally within a day), in a CI/CD pipeline

### Requirements
1. **Open source**
2. **Open license** (commercial use not restricted)
3. **Cross-platform, multi-language** (so that you can just drop this into a pipeline without needing to pick a specific tool for language X)
4. **No upselling for basic features** (for example, no paid upgrade required to cover all scans in a category)
5. **Usable in CI/CD pipelines** (i.e. via a CLI or API, and in a container)
6. **Should exit > 0 if issues are found** (ideally with configurable severity)

### CI/CD implementation
See `.gitlab-ci.yml`. Read on for command reference per category.

## Static code analysis
Tool: Semgrep

License: GNU Lesser GPL

Repo: https://github.com/returntocorp/semgrep

```
pip install semgrep
semgrep scan --config auto --exclude venv --error
# or from a container
docker run --rm -v "${PWD}:/src" returntocorp/semgrep semgrep scan --config auto --exclude venv --error
```
- Note: has a paid version which mostly seems for dashboards, but the CLI is usable without any account

## Open source libraries
Tool: Trivy

License: Apache

Repo: https://github.com/aquasecurity/trivy

```
docker run \
  -v $PWD:/workspace \
  aquasec/trivy \
  filesystem /workspace \
  --skip-dirs venv \
  --include-dev-deps \
  --severity MEDIUM,HIGH,CRITICAL \
  --exit-code 1
```
- Trivy can also scan container images and open source libraries in one go (see below)
- `--include-dev-deps` is only useful for npm and yarn (and therefore not this example repo), but is included here for reference.

## Containers
Tool: Trivy

License: Apache

Repo: https://github.com/aquasecurity/trivy

```
# Building with kaniko so we don't need an insecure Docker socket or DinD
docker run \
    -v $PWD:/workspace \
    gcr.io/kaniko-project/executor:latest \
    --no-push \
    --destination app \
    --tar-path app.tar
# Scan with Trivy
docker run \
  -v $PWD:/workspace \
  aquasec/trivy \
  image \
  --input /workspace/app.tar \
  --severity HIGH,CRITICAL \
  --exit-code 1 \
  --exit-on-eol 2
```
- `--exit-on-eol 2` makes it fail not just on vulnerabilities but also EOL OS distributions (such as Alpine 3.12 in this case)
- Also scans open source libraries (so in this case Python packages), meaning you can scan both the container and libraries in one go.
- Trivy can also scan Dockerfiles for misconfiguration 
  - For example: `docker run -v $PWD:/workspace aquasec/trivy config /workspace --skip-dirs venv --file-patterns dockerfile:Dockerfile`
  - Note that this also picks up the Cloudformation stack, even though the file-patterns flag is given. Hence it being experimental.
- Checkov (see below) could have also been used, but requires a paid upgrade for anything beyond basic linting of the Dockerfile (i.e. container runtime scanning, base image vulnerabilities, etc.)
  - Do note that basic linting of the Dockerfile is still wise to do with Checkov, as Trivy's config scanning seems to be in the experimental stage

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
- Trivy also picks up misconfigrations for the Cloudformation stack (just as the Dockerfile, as described above). Note that this seems to be experimental:
  - `docker run -v $PWD:/workspace aquasec/trivy config /workspace --skip-dirs venv`

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
