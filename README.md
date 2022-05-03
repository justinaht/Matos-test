![Matos Logo](./images/matos-logo.png)

![GitHub release (latest by date)](https://img.shields.io/github/v/release/matos/matos)
![GitHub Downloads](https://img.shields.io/github/downloads/matos/matos/total?logo=github&logoColor=white)
[![Go Report Card](https://goreportcard.com/badge/github.com/matos/matos)](https://goreportcard.com/report/github.com/matos/matos)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/3588/badge)](https://bestpractices.coreinfrastructure.org/projects/3588)

Matos is a cloud resource anomaly detection application. It helps detect anomalies; configuration and policy drifts. It interacts with native cloud services api's or third party tools to deduce current status and metadata of underlying resources and represents current security and compliance posture, one use case at a time. Inherently supports Amazon Web Services and Google Cloud Platform services. Resource support and use cases will be extended as a part of planned road map.

## Features

- Support AWS and GCP
- Get current real time resource information and metadata
- Identify anomalies and policy/configuration drifts

## Future Enhancements

- Extend
  - Support to more resources and Services
  - Detection scope for more use cases
  - Support for more cloud platforms
- Get health information and compare against set/defined thresholds
- Recommend remediation for detected anomalies and drifts

## Documentation & Support

- [Quickstart](./docs/QUICKSTART.md)
- [Community](./docs/COMMUNITY.md)
- [Code of Conduct](./docs/CODE_OF_CONDUCT.md)
- [Maintainers](./docs/MAINTAINERS.md)
  - [CodeOwners](./docs/CODEOWNERS.md)
  - [Contribution Guidelines](./docs/CONTRIBUTION_GUIDELINES.md)
  - [Security](./docs/SECURITY.md)
- [License](./docs/LICENSE.md)

## Contents

Directory|Description
-|-
[api](api) | API model, routes and schema definitions module
[credentials](credentials)| Cloud account credential json files for authentication and authorization
[docs](docs) | Matos project documents
[images](images) | Matos project image assets
[providers](providers) | Cloud Service Provider discovery, observability module
[services](services) | Cloud Infrastructure resource service module
[test](test) | Matos project test cases and data 
[utils](utils) | Utility library module

# Disclaimer

Matos does not save, publish or share with anyone any identifiable confidential information.

# Support

Cloudmatos builds and maintains Matos to make deep observability and policy checks simple and accessible.
Start with our Documentation for quick start and tests.
If you need direct support you can contact us at [community@cloudmatos.com](mailto:community@cloudmatos.com).
