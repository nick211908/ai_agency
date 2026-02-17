#!/bin/bash

set -e

PROJECT_NAME="ai-agency-platform"

echo "Creating project: $PROJECT_NAME"

mkdir -p $PROJECT_NAME && cd $PROJECT_NAME

# -----------------------------
# ROOT LEVEL
# -----------------------------
touch README.md .env .gitignore docker-compose.yml Makefile

mkdir -p services modules workers shared infra scripts tests

# -----------------------------
# SERVICES
# -----------------------------
SERVICES=(
  api-gateway
  job-service
  pipeline-service
  llm-service
  tool-service
  evaluation-service
  auth-service
  storage-service
)

for SERVICE in "${SERVICES[@]}"; do
  mkdir -p services/$SERVICE/app/{routes,services,models,schemas,config}
  touch services/$SERVICE/app/main.py
  touch services/$SERVICE/requirements.txt
  touch services/$SERVICE/Dockerfile
done

# Special structure for pipeline-service
mkdir -p services/pipeline-service/app/engine
mkdir -p services/pipeline-service/app/steps

touch services/pipeline-service/app/engine/{executor.py,registry.py,state.py,scheduler.py}
touch services/pipeline-service/app/steps/{normalize.py,retrieve.py,generate.py,evaluate.py,refine.py,format.py}

# Special structure for llm-service
mkdir -p services/llm-service/app/providers
mkdir -p services/llm-service/app/router

touch services/llm-service/app/providers/{openai.py,anthropic.py,local_llm.py}
touch services/llm-service/app/router/model_router.py

# Special structure for tool-service
mkdir -p services/tool-service/app/tools
touch services/tool-service/app/tools/{pdf_generator.py,ffmpeg_tool.py,scraper.py,formatter.py}

# Special structure for evaluation-service
mkdir -p services/evaluation-service/app/evaluators
mkdir -p services/evaluation-service/app/rules

touch services/evaluation-service/app/evaluators/{llm_judge.py,rule_engine.py,hybrid.py}
touch services/evaluation-service/app/rules/{legal_rules.py,ad_rules.py}

# Special structure for auth-service
mkdir -p services/auth-service/app/middleware
touch services/auth-service/app/middleware/auth_guard.py

# Special structure for storage-service
mkdir -p services/storage-service/app/services
touch services/storage-service/app/services/{s3_client.py,file_manager.py}

# -----------------------------
# MODULES (Domain Logic)
# -----------------------------
mkdir -p modules/legal/{pipelines,prompts,rules,schemas,knowledge,agents}
mkdir -p modules/ads
mkdir -p modules/seo

touch modules/legal/pipelines/legal_pipeline.py
touch modules/legal/prompts/{drafting.txt,compliance.txt,risk.txt}
touch modules/legal/rules/compliance_rules.py
touch modules/legal/schemas/contract_schema.py
touch modules/legal/agents/{planner.py,drafter.py,checker.py,analyzer.py}

# -----------------------------
# WORKERS
# -----------------------------
mkdir -p workers/{pipeline-worker,tool-worker,evaluation-worker}

for WORKER in pipeline-worker tool-worker evaluation-worker; do
  touch workers/$WORKER/worker.py
  touch workers/$WORKER/tasks.py
done

# -----------------------------
# SHARED
# -----------------------------
mkdir -p shared/{schemas,utils,clients,constants,events}

touch shared/schemas/{job.py,task.py,pipeline.py,response.py}
touch shared/utils/{logger.py,retry.py,config.py,exceptions.py}
touch shared/clients/{redis_client.py,kafka_client.py,postgres_client.py,vector_db.py}
touch shared/constants/enums.py
touch shared/events/{event_types.py,producer.py,consumer.py}

# -----------------------------
# INFRA
# -----------------------------
mkdir -p infra/{docker,k8s,terraform}

touch infra/k8s/{deployment.yaml,service.yaml,ingress.yaml}
touch infra/terraform/main.tf

# -----------------------------
# SCRIPTS
# -----------------------------
mkdir -p scripts
touch scripts/dev.sh

# -----------------------------
# TESTS
# -----------------------------
mkdir -p tests/{unit,integration}

# -----------------------------
# GITIGNORE
# -----------------------------
cat <<EOL > .gitignore
__pycache__/
*.pyc
.env
.venv/
node_modules/
dist/
build/
*.log
EOL

echo "Project structure created successfully!"
