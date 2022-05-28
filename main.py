# this is not overcommented at all
import re,requests,os,time,random,logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s')

outputDir = "unity2d_all"
# i should make the output dir name configurable, but i'm lazy
version = str(input('Version (Find it at https://play.google.com/store/apps/details?id=jp.enish.gotopazu, then open the "About this game" option, https://files.catbox.moe/et7cek.png and https://files.catbox.moe/k3iwsp.png for reference): '))
# i should make this a gui, but i'm lazy and i don't know how
# i should get the version from the website, but i'm lazy
# i should make it remember the last entered version, but i'm lazy
version = version.replace('.', '_')
logging.info(f"Version: {version}")
if not version:
    logging.info('No version specified, exiting...')
    exit()
    # no version specified, exit
url = f"https://www-cancer.enish-games.com/v{version}/resource/list/Android"
logging.info(f"Download url: {url}")
response = requests.get(url).text
if "メンテナンス中" in response:
    raise Exception("Server is in maintenance")
    # server is in maintenance, exit
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
    # create output directory if it doesn't exist
fileNames = set(re.findall(r"[0-9a-f]{32}", response))
# find all file names in the response
finddir = set(os.listdir("unity2d_all"))
# find all file names in the output directory
filelist = list(fileNames-finddir)
# find the difference between the two sets
for file in filelist:
    if file in outputDir:
        logging.info(f"{file} already exists")
        continue
        # if file already exists, skip
    else:
        url = f"https://assets.enish-games.com/assets-cancer/Resources/android/{file}"
        logging.info(f"Downloading {file}")
        os.system(
            " ".join([
                'wget',
                '--random-wait',
                '--no-check-certificate',
                '-q',
                '-nv',
                '-c',
                '-N',
                f'--user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53"',
                url,
                '-P',
                outputDir
            ])
        )
        time.sleep(random.uniform(0.1, 1))
        logging.info(f"{file} downloaded")
        # download file and log it
if not file in filelist:
    logging.info("All files are downloaded")
    exit()
    # all files are downloaded, exit
# cant believe all this actually works
# hey, if you're reading this, i hope you know what you're doing, because i don't, so don't complain