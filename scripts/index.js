const puppeteer = require('puppeteer');
const args = process.argv;
const utils = require('./utils')


puppeteer.launch().then(async browser =>{
    let token = ''
    const directory = args[2]
    const main_url = args[3]
    const is_staging = args[4]

    if (is_staging == undefined) {
        token = utils.generate_token()
    }

    let slice_url = utils.slice_url(main_url)
    let slash_slice_url = utils.slash_slice_url(slice_url)
    let url = utils.create_url(slash_slice_url, token)
    let path = utils.clean_url(slash_slice_url)

    try {
            const page = await browser.newPage();
            page.setViewport({width: 1280, height: 1024})
            await page.goto(url, {waitUntil: 'networkidle'})
            let file_path = utils.file_path(directory, path)
            await page.screenshot({path: file_path, fullPage:true})
            console.log(main_url)
        }
        catch (err) {
            let fail_url = utils.fail_screenshot(main_url)
            console.log(fail_url)
        }
    await browser.close();
})
