# gcloud auth

## Setting up local gcloud config

First, set the `GCP_PROJECT` variable in the [.env](../../.env) to your new project id.

Run the one-time setup of the Google Cloud project config.

```sh
make gcloud_init
```

Activate the project config and handle auth. If you work on multiple projects, you'll need to run this each time you switch projects.

This also sets up a [docker credential helper](https://cloud.google.com/artifact-registry/docs/docker/authentication) so you can push docker images to the project's Google Container Registry.

```sh
make gcloud_login
```

This will ask you (twice) to go to a URL in your browser in order to login with your email address that created the project, and then you'll need to copy+paste a key from your browser into the terminal. This is annoying, but it's setting up your normal user auth as well as [application default credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev).
