## Download and Install Docker

Follow the instructions here to download and install Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/).

## Makefile Targets for Docker

1. Build the Docker image: `make build`
2. Run the Docker image locally: `make start` (available at [http://localhost:8080](http://localhost:8080))
3. Stop the Docker image: `make stop`
4. View docker logs (while container is running): `make logs`
5. Run all tests other than the LLM tests: `make test`
6. Run all tests including LLM tests: `make test_all`

## Build and Push the Vertex AI Billing app's docker image

To deploy in Cloud Run, we need a docker image in Google Container Registry. To build and push the image, run the following command:

```sh
make push_image
```
