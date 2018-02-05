const utils = require('../scripts/utils')


test('get token generated', () => {
    const spy = jest.spyOn(utils, 'generate_token')
    utils.generate_token()

    expect(spy).toHaveBeenCalled()
});

test('get url with url no threshold', () => {
    main_url = 'http://www.prontomarketing.in.th/'

    let result = utils.slice_url(main_url)
    expected = 'http://www.prontomarketing.in.th'
    expect(result).toBe(expected)
});

test('get url with url and has threshold', () => {
    main_url = 'http://www.prontomarketing.in.th/,0.03'

    let result = utils.slice_url(main_url)
    expected = 'http://www.prontomarketing.in.th'
    expect(result).toBe(expected)
});

test('fix url by add slash at the end', () => {
    slice_url = 'https://www.prontomarketing.in.th'

    let result = utils.slash_slice_url(slice_url)
    expected = 'https://www.prontomarketing.in.th/'
    expect(result).toBe(expected)
})

test('create url that merge with token', () => {
    slash_slice_url = 'https://www.prontomarketing.in.th/'
    token= '0.03.04'

    let result = utils.create_url(slash_slice_url, token)
    expected = 'https://www.prontomarketing.in.th/?0.03.04'
});

test('get url with no http and slash', () => {
    raw_path_url = 'http://www.prontomarketing.in.th/'

    let result = utils.clean_url(raw_path_url)
    expected = 'www.prontomarketing.in.th_'
    expect(result).toBe(expected)
});

test('get url with no https and slash with token', () => {
    raw_path_url = 'https://www.prontomarketing.in.th/?0.301.303'

    let result = utils.clean_url(raw_path_url)
    expected = 'www.prontomarketing.in.th_?0.301.303'
    expect(result).toBe(expected)
});

test('get file path name', () => {
    directory = 'before'
    path = 'www.prontomarketing.in.th_'

    let result = utils.file_path(directory, path)
    expected = 'before/www.prontomarketing.in.th_.png'
    expect(result).toBe(expected)
})

test('get fail screenshot message', () => {
    const main_url = 'https://www.prontomarketing.in.th/'
    expected = 'https://www.prontomarketing.in.th/ ############################## Fail Screenshot ##############################'

    let result = utils.fail_screenshot(main_url)
    expect(result).toBe(expected)
});
