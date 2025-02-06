const puppeteer = require('puppeteer');
const fs = require('fs');

async function renderToImage(htmlFile, imageFile) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    await page.goto(`file://${process.cwd()}/${htmlFile}`, { waitUntil: 'networkidle2' });
    await page.screenshot({ path: imageFile, fullPage: true });

    await browser.close();
}

const args = process.argv.slice(2);
if (args.length < 2) {
    console.error("Usage: node render.js <htmlFile> <imageFile>");
    process.exit(1);
}

renderToImage(args[0], args[1])
    .then(() => console.log("Image saved"))
    .catch(err => console.error(err));
