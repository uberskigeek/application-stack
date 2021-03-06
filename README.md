<!-- PROJECT LOGO -->

<p align="center">
  <a href="https://openliberty.io/">
    <img src="https://openliberty.io/img/spaceship.svg" alt="Logo">
  </a>
</p>
<p align="center">
  <a href="https://openliberty.io/">
    <img src="https://github.com/OpenLiberty/open-liberty/blob/master/logos/logo_horizontal_light_navy.png" alt="title" width="400">
  </a>
</p>
<br />


[![License](https://img.shields.io/badge/License-EPL%201.0-green.svg)](https://opensource.org/licenses/EPL-1.0)

# Summary

A devfile-based application stack for Open Liberty

## Contributing

Our [CONTRIBUTING](https://github.com/OpenLiberty/application-stack/blob/master/CONTRIBUTING.md) document contains details for submitting pull requests.

# Open Liberty Application Stack

The Open Liberty application stack provides a consistent way of developing microservices based upon the [Jakarta EE](https://jakarta.ee/) and [Eclipse MicroProfile](https://microprofile.io) specifications. This stack lets you use [Maven](https://maven.apache.org) to develop applications for [Open Liberty](https://openliberty.io) runtime, that is running on OpenJDK with container-optimizations in OpenJ9.

This stack is based on OpenJDK with container-optimizations in OpenJ9 and `Open Liberty v20.0.0.3`. It provides live reloading during development by utilizing the ["dev mode"](https://openliberty.io/blog/2019/10/22/liberty-dev-mode.html) capability in the liberty-maven-plugin.  

**Note:** Maven is provided by the stack, allowing you to build, test, and debug your Java application without installing Maven locally. However, we recommend installing Maven locally for the best development experience.

## Default template

The default template provides a `pom.xml` file that enables Liberty features that support [Eclipse MicroProfile 3.2](https://openliberty.io/docs/ref/feature/#microProfile-3.2.html). Specifically, this template includes:

#### Health

The `mpHealth` feature allows services to report their readiness and liveness status - UP if it is ready or alive and DOWN if it is not ready/alive. It publishes two corresponding endpoints to communicate the status of liveness and readiness. A service orchestrator can then use the health statuses to make decisions.

Liveness endpoint: http://localhost:9080/health/live
Readiness endpoint: http://localhost:9080/health/ready

#### Metrics

The `mpMetrics` feature enables MicroProfile Metrics support in Open Liberty. Note that this feature requires SSL and the configuration has been provided for you. You can monitor metrics to determine the performance and health of a service. You can also use them to pinpoint issues, collect data for capacity planning, or to decide when to scale a service to run with more or fewer resources.

Metrics endpoint: http://localhost:9080/metrics

##### Metrics Password

Log in as the `admin` user to see both the system and application metrics in a text format.   The password for this `admin` user will be generated by the container.  

To get the generated password for project **my-project**, you can exec in the container like this, for example:

    $ docker exec -it my-project-dev  bash -c "grep keystore /opt/ol/wlp/usr/servers/defaultServer/server.env"

    keystore_password=2r1aquTO3VVUVON7kCDdzno

So in the above example the password value would be: `2r1aquTO3VVUVON7kCDdzno`

#### OpenAPI

The `mpOpenAPI` feature provides a set of Java interfaces and programming models that allow Java developers to natively produce OpenAPI v3 documents from their JAX-RS applications. This provides a standard interface for documenting and exposing RESTful APIs.

OpenAPI endpoints:
- http://localhost:9080/openapi (the RESTful APIs of the inventory service)
- http://localhost:9080/openapi/ui (Swagger UI of the deployed APIs)

#### Junit 5

The default template uses JUnit 5. You may be used to JUnit 4, but here are some great reasons to make the switch https://developer.ibm.com/dwblog/2017/top-five-reasons-to-use-junit-5-java/


## Getting Started

1. Perform an `oc login` to your Open Shift cluster for development purposes.

2.  Get the [odo v.1.2.1](https://mirror.openshift.com/pub/openshift-v4/clients/odo/v1.2.1/) CLI (or later).

1. Create a new folder in your local directory and initialize it using the Odo CLI, e.g.:
    ```bash
    mkdir my-project
    cd my-project
    odo create --downloadSource
    ```
    Provide a name for the project when prompted
    identify the Open Shift namespace to be used
    
    This will initialize an Open Liberty project and download the default template.

1. Once your project has been initialized, you can run your application using the following command:

    ```bash
    odo watch 
    ```
    
    Upon first time invocation, this initializes an Open Shift managed kubernetes pod, launches a Docker container in that pod and  syncs your source code to that container. Finally, this will start your application, exposing it on port 9080 of the container. 
    
    This command is making use of an odo watcher that will will recieve notification when any source ile within the project is updated and saved. 

1. To access your application from the host, you must create an Open Shift URL connection to the container by using the following command:
    ```bash
    odo url create --port 9080
    odo push
    ```
    The url will take the form of `<project name>-9080-<namespace>`
    
    You can continue to edit the application in your preferred IDE (Eclipse, VSCode or others) and your changes will be reflected in the running container within a few seconds.

1. You should be able to access the following endpoints, as they are exposed by your template application by default:

    - Readiness endpoint: http://`<project name>-9080-<namespace>.<host-ip>`/health/ready
    - Liveness endpoint: http://`<project name>-9080-<namespace>.<host-ip>`/health/live
    - Metrics endpoint: http://`<project name>-9080-<namespace>.<host-ip>`/metrics (login as `admin` user with password obtained as mentioned [here](#Metrics-Password).
    - OpenAPI endpoint: http://`<project name>-9080-<namespace>.<host-ip>`/openapi
    - Swagger UI endpoint: http://`<project name>-9080-<namespace>.<host-ip>`/openapi/ui

## Odo local development operations: (run/debug/test )

### RUN
If you launch via `odo push` then the liberty-maven-plugin will launch dev mode in "hot test" mode, where unit tests and integration tests get automatically re-executed after each detected change. You must have visibility to the logs on the Open Shift container to see these test results.  

### DEBUG
Not currently supported

### TEST
Not currently supported

## License

Usage is provided under the [EPL 1.0 license](https://opensource.org/licenses/EPL-1.0) See LICENSE for the full details.

