# Project and Infrastructure Setup

This repo handles enabling the Google Cloud APIs you need in order to run the Vertex AI Billing service, as well as creating a relatively minimally scoped service account to attach to it.

After setting up your local environment (docker), run the following command from the root of the repository to see what Terraform will handle for you:
```sh
make terraform_plan
```

When you're comfortable with the changes Terraform is going to make, run the following command to apply them:
```sh
make terraform_apply
```

To destroy everything when you're finished working with this repo, run the following command:
```sh
make terraform_destroy
```

To only destroy the Vertex AI Billing service, run the following command:
```sh
make terraform_destroy_vertex_ai_billing_service
```
