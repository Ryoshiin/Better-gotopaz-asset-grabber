import re,requests,os,time,random,logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s')

outputDir = "unity2d_all"
version = str(input('Version (Find it at https://play.google.com/store/apps/details?id=jp.enish.gotopazu, then open the "About this game" option, https://files.catbox.moe/et7cek.png and https://files.catbox.moe/k3iwsp.png for reference): '))
version = version.replace('.', '_')
print(version)
if not version:
    print('No version specified, exiting...')
    exit()
url = f"https://www-cancer.enish-games.com/v{version}/resource/list/Android"
print(url)
response = requests.get(url).text
print(response)
if "メンテナンス中" in response:
    raise Exception("Server is in maintenance")
if not os.path.exists(outputDir):
    os.mkdir("unity2d_all")
fileNames = set(re.findall(r"[0-9a-f]{32}", response))
finddir = set(os.listdir("unity2d_all"))
filelist = list(fileNames-finddir)
print(filelist)
for file in filelist:
    if file in outputDir:
        logging.info(f"{file} already exists")
        continue
    else:
        url = "https://assets.enish-games.com/assets-cancer/Resources/android/"+file
        os.system(
            " ".join([
                'wget',
                '--random-wait',
                '--no-check-certificate',
                '-c',
                '-N',
                f'--user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53"',
                url,
                '-P',
                outputDir
            ])
        )
        time.sleep(random.uniform(0.1, 1))