pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        VITE_API_URL = 'http://localhost:8000'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend validation') {
            steps {
                dir('app/backend') {
                    sh '''
                        set -eux

                        python3 -m venv .venv
                        . .venv/bin/activate

                        python -m pip install --upgrade pip
                        pip install -r requirements.txt

                        python -m compileall app

                        APP_ENV=ci \
                        DATABASE_URL=sqlite:///./test_legacyops.db \
                        REDIS_REQUIRED=false \
                        pytest -q

                        APP_ENV=ci \
                        DATABASE_URL=postgresql+psycopg2://legacyops:legacyops@localhost:5432/legacyops \
                        REDIS_URL=redis://localhost:6379/0 \
                        REDIS_REQUIRED=false \
                        python -c "from app.main import app; print('Backend import OK:', app.title)"
                    '''
                }
            }
        }

        stage('Frontend validation') {
            steps {
                sh '''
                    set -eux

                    docker run --rm \
                        -u "$(id -u):$(id -g)" \
                        -e VITE_API_URL="${VITE_API_URL}" \
                        -v "$PWD:/workspace" \
                        -w /workspace/app/frontend \
                        node:22-alpine \
                        sh -c 'npm ci && npm run build'
                '''
            }
        }

        stage('Docker Compose validation') {
            steps {
                sh '''
                    set -eux

                    docker compose down -v --remove-orphans || true
                    docker compose config
                    docker compose build
                    docker compose up -d
                    docker compose ps

                    timeout 90 bash -c 'until curl -fsS http://localhost:8000/health; do sleep 2; done'
                    curl -fsSI http://localhost:3000
                '''
            }
        }
    }

    post {
        always {
            sh 'docker compose down -v --remove-orphans || true'
        }
    }
}
