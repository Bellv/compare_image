# Compare before and after page tool #

## Concept behind this tool
Nowadays, when we upgrade plugins and core, we don't know if they would be broken or not. This tool helps to collect the screenshots before and after upgrade site. These screenshots can be compared the different before and after upgrading.


## How to use this tool
1. Run `pip install -r requirements.txt` and `yarn -g install` (Do only 1st time)
2. Add pages to `site.txt` each page per line
3. Before upgrading, run `./scripts/screenshot.sh before` to collect screenshots to `before` directory
4. After upgrading, run `./scripts/screenshot.sh after` to collect screenshots to `after` directory
5. For setting hosts file site, you need to add `ip` and `domain` in `/etc/host` file for access specific site on staging server. After host file setting, we can add `staging` behind the screenshot script command to ignore query string cache process.
```
Ex. ./scripts/screenshot.sh before staging
```
6. Run `python scripts/compare_script.py` to compare screenshots and get the result
7. You can Add `,x.xx` after site url where x is number for percentage of threshold in `site.txt`
```
By 0.01 = 1%, 0.5 = 50% and 1 = 100%
Ex. http://bossyong.bypronto.com/,0.02
```
7. Use `./scripts/clear.sh` to remove all file in `before`, `after` and `report` directory.

## How to run test
1. Use command `python -m unittest discover tests/` to test Python part
2. Use `npm test` to test javascript part
