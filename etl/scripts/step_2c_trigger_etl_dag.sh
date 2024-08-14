PROJECT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_PATH=$(dirname "$PROJECT_PATH")
PROJECT_PATH=$(dirname "$PROJECT_PATH")

source $PROJECT_PATH/.env

gcloud composer environments run $COMPOSER_ENV_NAME \
    --location=$COMPOSER_ENV_REGION \
    dags trigger -- anime_etl_pipeline