pipeline {
    agent any

    environment {
        // Esto crea una ruta temporal hacia el archivo secreto
        ENV_FILE = credentials('api-env-file')
    }

    stages {
        stage('Setup Environment') {
            steps {
                // Copiamos el archivo secreto al directorio de trabajo como ".env"
                sh 'cp $ENV_FILE .env'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install --break-system-packages -r requirements.txt'
            }
        }

        stage('Unit Tests') {
            steps {
                // Generamos un reporte de tests si quieres (opcional)
                sh 'set -o pipefail; python manage.py test | tee tests_report.txt'
            }
        }

        stage('Security: Dependencies (pip-audit)') {
            steps {
                // 'tee' muestra el resultado en pantalla Y lo guarda en el archivo
                // PIPESTATUS asegura que si pip-audit falla, el stage falle
                sh 'set -o pipefail; pip-audit | tee audit_report.txt'
            }
        }

        stage('Security: Code (Bandit)') {
            steps {
                sh 'set -o pipefail; bandit -r . -x ./venv,./**/tests.py -ll | tee bandit_report.txt'
            }
        }

        stage('Django Deployment Check') {
            steps {
                sh 'set -o pipefail; python manage.py check --deploy | tee check_report.txt'
            }
        }
    }

    post {
        always {
            // Esto guarda los archivos en el servidor de Jenkins para que los descargues
            archiveArtifacts artifacts: '*.txt', allowEmptyArchive: true
            echo 'Finalizando pipeline...'
        }
        failure {
            echo '❌ La validación ha fallado. Revisa los archivos guardados en "Artifacts".'
        }
    }
}