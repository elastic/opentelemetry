// Harmless PoC script to log GitHub Actions environment information
// This script will run during the docs-build workflow if the vulnerability exists

const fs = require('fs');
const path = require('path');

// Log file to store the results
const logFile = path.join(__dirname, 'workflow-info.log');

// Function to collect environment information
function collectEnvInfo() {
  const info = {
    timestamp: new Date().toISOString(),
    environment: {
      // Only collecting non-sensitive environment variables
      nodeVersion: process.version,
      platform: process.platform,
      arch: process.arch,
      cwd: process.cwd(),
      envVarsExist: Object.keys(process.env)
        .filter(key => !key.includes('SECRET') && !key.includes('TOKEN'))
        .sort()
    },
    // Check if we're running in GitHub Actions
    isGitHubActions: process.env.GITHUB_ACTIONS === 'true',
    workflowName: process.env.GITHUB_WORKFLOW || 'Not in GitHub Actions',
    eventName: process.env.GITHUB_EVENT_NAME || 'Not in GitHub Actions',
    repositoryName: process.env.GITHUB_REPOSITORY || 'Not in GitHub Actions',
    runId: process.env.GITHUB_RUN_ID || 'Not available',
    // Verify if we have PR context
    hasPrContext: !!process.env.GITHUB_EVENT_NAME && process.env.GITHUB_EVENT_NAME.includes('pull_request'),
    // Log workflow permissions (non-sensitive)
    workflowRef: process.env.GITHUB_WORKFLOW_REF || 'Not available',
    workflowSHA: process.env.GITHUB_SHA || 'Not available'
  };
  
  return info;
}

// Get the environment info
const envInfo = collectEnvInfo();

// Write to file
fs.writeFileSync(logFile, JSON.stringify(envInfo, null, 2));

// Also print to console for workflow logs
console.log('PoC Info Collection Complete');
console.log('======================================');
console.log(`Running in GitHub Actions: ${envInfo.isGitHubActions}`);
console.log(`Workflow Name: ${envInfo.workflowName}`);
console.log(`Event Name: ${envInfo.eventName}`);
console.log(`Repository: ${envInfo.repositoryName}`);
console.log(`Run ID: ${envInfo.runId}`);
console.log(`Has PR Context: ${envInfo.hasPrContext}`);
console.log('======================================');
console.log('Full details written to workflow-info.log');

// This script will execute during the build process if the vulnerability exists
// It only collects non-sensitive information to demonstrate code execution
