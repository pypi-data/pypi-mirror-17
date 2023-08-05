from rootfetch.base import *


class MozillaFetcher(RootStoreFetcher):

    # curl https://hg.mozilla.org/mozilla-central/raw-file/tip/security/nss/lib/ckfw/builtins/certdata.txt -o certdata.txt
    MOZILLA_URL = "https://hg.mozilla.org/mozilla-central/raw-file/tip/security/nss/lib/ckfw/builtins/certdata.txt"

    def fetch(self, output):
        raw_path = self._make_temp_path("rootfetch-mozilla-raw")
        urllib.urlretrieve(self.MOZILLA_URL, raw_path)
        cabe_path = self._make_temp_path("rootfetch-microsoft-cab-extracted")
        subprocess.check_call("extract-nss-root-certs %s > %s" % (raw_path, cabe_path), shell=True)
        with open(cabe_path) as fd:
            output.write(fd.read())


if __name__ == "__main__":
    m = MozillaFetcher()
    m.setup()
    m.fetch(sys.stdout)
