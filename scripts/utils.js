function generate_token() {
    return `?${Math.random().toString(36)}`
}

function slice_url(main_url) {
    return main_url.slice(0, main_url.indexOf('/,'))
}

function slash_slice_url(slice_url) {
    return `${slice_url}/`
}

function create_url(slash_slice_url, token) {
    return `${slash_slice_url}${token}`
}

function clean_url(slash_slice_url) {
    return slash_slice_url.replace('http://', '').replace('https://', '').replace(/\//g, '_')
}

function file_path(directory, path) {
    return `${directory}/${path}.png`
}

function fail_screenshot(main_url) {
    return `${main_url} ############################## Fail Screenshot ##############################`
}

module.exports = {
    generate_token,
    slice_url,
    slash_slice_url,
    create_url,
    clean_url,
    file_path,
    fail_screenshot
}
