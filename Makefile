# ==================== [START] Global Variable Declaration =================== #
SHELL := /bin/bash
BASE_DIR := $(shell pwd)

OPERATING_SYSTEM := $(shell uname -s)

APP_URL := http://127.0.0.1:8080

include .env

export
# ===================== [END] Global Variable Declaration ==================== #

# ========================== [START] Docker Targets ========================== #
IMAGE_TAG ?= latest
build:
	@docker compose -f docker-compose.yml build vertex-ai-billing

push_image: build
	@docker push gcr.io/$(GCP_PROJECT)/vertex-ai-billing:$(IMAGE_TAG)
	@docker compose -f support/gcloud/docker-compose.yml run --rm -it gcloud bash -c "/mnt/project/support/replace_env_value.sh VERTEX_AI_BILLING_SERVICE_IMAGE gcr.io/$(GCP_PROJECT)/vertex-ai-billing:$(IMAGE_TAG) /mnt/project/.env"

# usage example:
# - make logs
logs:
	@docker compose logs -f vertex-ai-billing

# usage examples:
# - make start build=true chrome=true
# - make start firefox=true
start:
	$(info checking if image should rebuild...)
ifeq ($(build), true)
	@docker compose up --detach --build
else
	@docker compose up --detach
endif
	@([ $(OPERATING_SYSTEM) = "Darwin" ] && [ "$(chrome)" = "true" ])  && open -a "Google Chrome" "$(APP_URL)" || true
	@([ $(OPERATING_SYSTEM) = "Darwin" ] && [ "$(firefox)" = "true" ]) && open -a "Firefox"       "$(APP_URL)" || true
	@([ $(OPERATING_SYSTEM) = "Linux"  ] && ([ "$(chrome)" = "true" ] || [ "$(firefox)" = "true" ]) ) && xdg-open "$(APP_URL)" 2>/dev/null &

# usage example:
# - make stop
stop:
	@docker compose down

# usage example:
# - make test
test: build
	@env_running=$$(docker compose ps --status running | grep vertex-ai-billing > /dev/null 2>&1 && echo -n true);\
	([ "$(env_running)" = "true" ]) && docker compose exec -it vertex-ai-billing bash -c "cd /root/modules && coverage run -m pytest -v --ignore=helpers/llm && coverage report -m";\
	([ "$(env_running)" != "true" ]) && docker compose run --rm -it vertex-ai-billing bash -c "cd /root/modules && coverage run -m pytest -v --ignore=helpers/llm && coverage report -m";

# usage example:
# - make test_all
test_all: build
	@env_running=$$(docker compose ps --status running | grep vertex-ai-billing > /dev/null 2>&1 && echo -n true);\
	([ "$(env_running)" = "true" ]) && docker compose exec -it vertex-ai-billing bash -c "cd /root/modules && coverage run -m pytest -v && coverage report -m";\
	([ "$(env_running)" != "true" ]) && docker compose run --rm -it vertex-ai-billing bash -c "cd /root/modules && coverage run -m pytest -v && coverage report -m";

# usage example:
# - make test_one name=make test_one name=helpers/prompts/tests/test_bigquery.py
# - make test_one name=make test_one name=helpers/prompts/tests/test_visualization.py
# - make test_one name=make test_one name=helpers/llm/tests/test_visualization.py
test_one: build
	@env_running=$$(docker compose ps --status running | grep vertex-ai-billing > /dev/null 2>&1 && echo -n true);\
	([ "$(env_running)" = "true" ]) && docker compose exec -it vertex-ai-billing bash -c "cd /root/modules && coverage run -m pytest $(name) && coverage report -m";\
	([ "$(env_running)" != "true" ]) && docker compose run --rm -it vertex-ai-billing bash -c "cd /root/modules && coverage run -m pytest $(name) && coverage report -m";

# usage example:
# - make test_directory name=helpers/prompts
test_directory:
	@env_running=$$(docker compose ps --status running | grep vertex-ai-billing > /dev/null 2>&1 && echo -n true);\
	([ "$(env_running)" = "true" ]) && docker compose exec -it vertex-ai-billing bash -c "cd /root/modules && coverage run -m pytest -v $(name) && coverage report -m";\
	([ "$(env_running)" != "true" ]) && docker compose run --rm -it vertex-ai-billing bash -c "cd /root/modules && coverage run -m pytest -v $(name) && coverage report -m";
# =========================== [END] Docker Targets =========================== #


# ====================== [START] Infrastructure Targets ====================== #
# usage example:
# - make terraform_init
terraform_init:
	@docker compose -f terraform/docker-compose.yml run --rm -it terraform init

# usage example:
# - make terraform_plan
terraform_plan:
	@make terraform_init
	@docker compose -f terraform/docker-compose.yml run --rm -it terraform plan

# usage example:
# - make terraform_apply
terraform_apply:
	@make terraform_init
	@docker compose -f terraform/docker-compose.yml run --rm -it terraform apply
	@export API_KEY=$$(docker compose -f terraform/docker-compose.yml run --rm -it terraform output -raw custom_search_api_key);\
	docker compose -f support/gcloud/docker-compose.yml run --rm -it gcloud bash -c "/mnt/project/support/replace_env_value.sh GOOGLE_API_KEY $$API_KEY /mnt/project/.env";\
	docker compose -f support/gcloud/docker-compose.yml run --rm -it gcloud bash -c "/mnt/project/support/replace_env_value.sh GOOGLE_GEMINI_API_KEY $$API_KEY /mnt/project/.env"
	@export BUCKET_NAME=$$(docker compose -f terraform/docker-compose.yml run --rm -it terraform output -raw google_storage_bucket_name);\
	docker compose -f support/gcloud/docker-compose.yml run --rm -it gcloud bash -c "/mnt/project/support/replace_env_value.sh GCP_BUCKET_NAME $$BUCKET_NAME /mnt/project/.env"

# usage example:
# - make terraform_destroy
terraform_destroy:
	@docker compose -f terraform/docker-compose.yml run --rm -it terraform destroy

# run this if you only want to destroy the publicly accessible cloud run service
# and nothing else (such as the bigquery API and others that were enabled)
# usage example:
# - make terraform_destroy_vertex_ai_billing_service
terraform_destroy_vertex_ai_billing_service:
	@docker compose -f terraform/docker-compose.yml run --rm -it terraform destroy -target=module.vertex_ai_billing
# ======================= [END] Infrastructure Targets ======================= #


# =================== [START] Google Cloud Config Targets ==================== #
# usage example:
# - make gcloud_init
gcloud_init:
	@docker compose -f support/gcloud/docker-compose.yml run --rm -it gcloud bash -c 'gcloud config configurations create $$GCP_PROJECT'
	@docker compose -f support/gcloud/docker-compose.yml run --rm -it gcloud bash -c 'gcloud config set project $$GCP_PROJECT'

# usage example:
# - make gcloud_login
gcloud_login:
	@docker compose -f support/gcloud/docker-compose.yml run --rm -it gcloud bash -c 'gcloud config set project $$GCP_PROJECT'
	@docker compose -f support/gcloud/docker-compose.yml run --rm -it gcloud bash -c 'gcloud auth login'
	@docker compose -f support/gcloud/docker-compose.yml run --rm -it gcloud bash -c 'gcloud auth application-default login'
	@docker compose -f support/gcloud/docker-compose.yml run --rm -it gcloud bash -c 'gcloud auth configure-docker || echo "docker setup failed, but it was probably already configured"'
# ==================== [END] Google Cloud Config Targets ===================== #
