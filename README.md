# Open source security scanning quickstart for developers
### Goal
This repo aims to make getting started with security scanning on any software development project easy, ideally getting it running in a CI/CD pipeline within a day. Tools are selected for four different types of scans, and based on a set of requirements which should make them compatible with any (or at least most) projects.

### Requirements
I've picked the tools based on the following requirements:
1. **Open source** and actively maintained
2. **Open license** (commercial use not restricted)
3. **Cross-platform, multi-language** (so that you can just drop this into a pipeline without needing to pick a specific tool for language X)
4. **No upselling for basic features** (for example, no paid upgrade required to cover all scans in a category)
5. **Usable in CI/CD pipelines** (i.e. via a CLI or API, and in a container)
6. **Should exit > 0 if issues are found** (ideally with configurable severity)

### CI/CD implementation
There are currently two example implementations in Gitlab CI and GitHub Actions:
- **Gitlab CI**: `.gitlab-ci.yml` 
- **GitHub Actions**: `.github/workflows/pipeline.yml`
Any other files in this repo 

The repo itself is also mirrored to both Gitlab and GitHub:
- https://gitlab.com/tettaji/security-scanning-quickstart
- https://github.com/Triqqo/security-scanning-quickstart

### Types of scans and their examples
- [Static code analysis](#static-code-analysis) - example scans `app.py`
- [Open source libraries](#open-source-libraries) - example scans `requirements.txt`
- [Containers](#containers) - example scans an `image.tar` built via Kaniko from the `Dockerfile`
- [Infrastructure as Code](#infrastructure-as-code) - example scans `cloudformation.yml` and `Dockerfile`

Refer to each section for tool reference and how to run them locally, or refer to the [CI/CD implementation](#cicd-implementation) for CI/CD examples.

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
- Note: has a paid SaaS version, but the CLI is usable without any account

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
  - Note that basic linting of the Dockerfile is still wise to do with Checkov, as Trivy's config scanning seems to be in the experimental stage

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
- Trivy also picks up misconfigurations of the Cloudformation stack (just as the Dockerfile, as described above). Note that this seems to be experimental:
  - `docker run -v $PWD:/workspace aquasec/trivy config /workspace --skip-dirs venv`

## Other tools
These tools aren't included in the example pipelines, and I haven't tested them much, but they might be interesting to look at as an alternative to the ones listed above:

<details>
  <summary>Click to expand</summary>

### All-in-one tools
- ShiftLeft Scan: https://github.com/ShiftLeftSecurity/sast-scan
  - Doesn't handle static code analysis very well (misses sys.argv injection in app.py, even though it reports that there are no issues in code)
  - Can also scan Docker images, but the report is borked.
  - Uses several other tools as scanning engines (such as Checkov) based on which files it detects
- Megalinter: https://github.com/oxsecurity/megalinter
  - Not just focused on security
  - Uses several other tools as scanning engines (such as Checkov) based on which files it detects

</details>
