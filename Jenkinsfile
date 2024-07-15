pipeline {
    agent any
  
    environment {
        MAIN_PROJECT = "${JOB_NAME.split('/')[-2]}"
        FOLDER_PART1 = "${JOB_NAME.split('/')[0]}"
        FOLDER_PART2 = "${JOB_NAME.split('/')[1]}"
        ACCESS_TOKEN = credentials('github-token')
        GITHUB_REPO = 'Xilinx/kria-dashboard'
        PR_NUMBER = "${env.CHANGE_ID}"
        REDIRECT_URL = "${JENKINS_URL}job/${FOLDER_PART1}/job/${FOLDER_PART2}/job/${MAIN_PROJECT}/view/change-requests/job/PR-${PR_NUMBER}/${BUILD_NUMBER}/console"
    }

    stages {
        stage('Initialization') {
            steps {
                script {
                    // echo "FOLDER_NAME: ${env.FOLDER}"    
                    echo "JENKINS_URL: ${env.JENKINS_URL}"
                    echo "MAIN_PROJECT: ${env.MAIN_PROJECT}"
                    echo "FOLDER_PART1: ${env.FOLDER_PART1}"
                    echo "FOLDER_PART2: ${env.FOLDER_PART2}"
                    echo "JOB_NAME: ${env.JOB_NAME}"
                    echo "JOB_BASE_NAME: ${env.JOB_BASE_NAME}"
                    echo "This is job name resided in the folder: ${env.MAIN_PROJECT}"
                    echo "REDIRECT_URL: ${env.REDIRECT_URL}"
                    postComment(env.PR_NUMBER, "URL of the PR: ${env.REDIRECT_URL}")
                }
            }
        }
      
        stage('echoing') {
            steps {
                script { 
                    sh "python3 --version"
                }
            }
        }
        stage('license-check') {
            steps {
                script {
                    // Run the license.py script and capture the output
                    def scriptOutput = sh(script: "python3 license.py  ${env.PR_NUMBER} '${env.ACCESS_TOKEN}'", returnStdout: true).trim()

                    if (scriptOutput.contains("License Check is Passed") || scriptOutput.contains("Skipping License Check for this File") || scriptOutput.contains("This is the Approved License. Hence, License Check is Passed")) {
                        currentBuild.result = "SUCCESS"
                    } else {
                        currentBuild.result = "FAILURE"
                    }
                    // Post the result on GitHub
                    postComment(env.PR_NUMBER, scriptOutput)
                    setGitHubCommitStatus(currentBuild.result)

                }
            }
        }
    }
}//endofpipeline

def postComment(prNumber, comment) {
    // Construct JSON body using JsonOutput.toJson method
    def jsonBody = groovy.json.JsonOutput.toJson(["body": comment])
    
    // Execute curl command to post the comment
    sh """
        curl -X POST \\
        -H 'Authorization: token ${env.ACCESS_TOKEN}' \\
        -H 'Content-Type: application/json' \\
        -d '${jsonBody}' \\
        https://gitenterprise.xilinx.com/api/v3/repos/${env.GITHUB_REPO}/issues/${prNumber}/comments
    """
}

def setGitHubCommitStatus(buildResult) {
    sh """
        curl -X POST \\
        -H "Authorization: token ${env.ACCESS_TOKEN}" \\
        -H "Accept: application/vnd.github.v3+json" \\
        https://gitenterprise.xilinx.com/api/v3/repos/${env.GITHUB_REPO}/statuses/${env.GIT_COMMIT} \\
        -d '{ "state": "${buildResult.toLowerCase()}", "description": "${buildResult}", "context": "Jenkins CI" }'
    """
}
