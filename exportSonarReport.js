const fs = require('fs');
const puppeteer = require('puppeteer');

const outputDirectory = 'https://github.com/sruthi3526/calcwebapp.git/'; // Change this to the absolute path of your Git repository

async function exportSonarReport() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Replace 'http://your-sonarqube-url' with the actual URL of your SonarQube server
  const sonarQubeUrl = 'http://localhost:9000';

  // Navigate to the SonarQube project dashboard
  await page.goto(`${sonarQubeUrl}/dashboard?id=com.cruds.demo:calcwebapp`);

  // Adjust the viewport and wait for any asynchronous content to load
  await page.setViewport({ width: 1200, height: 800 });
  await page.waitForTimeout(5000); // Adjust the wait time based on your project's load time

  // Capture a screenshot
  await page.screenshot({ path: `${outputDirectory}/sonar_report.png` });

  await browser.close();
}

exportSonarReport();
