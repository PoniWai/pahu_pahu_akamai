import os
import gc
from lib.httpclient import HttpClient


class OTAUpdater:
    """
    A class to update your MicroController with the latest version from a GitHub tagged release,
    optimized for low power usage.
    """
    def __init__(self, github_repo, github_src_dir='', module='', main_dir='app', new_version_dir='next', headers={}):
        self.http_client = HttpClient(headers=headers)
        self.github_repo = github_repo.rstrip(
            '/').replace('https://github.com/', '')
        self.github_src_dir = '' if len(
            github_src_dir) < 1 else github_src_dir.rstrip('/') + '/'
        self.module = module.rstrip('/')
        self.main_dir = main_dir
        self.new_version_dir = new_version_dir

    def __del__(self):
        self.http_client = None

    def install_update_if_available(self) -> bool:
        """This method will immediately install the latest version if out-of-date.

        This method expects an active internet connection and allows you to decide yourself
        if you want to install the latest version. It is necessary to run it directly after boot 
        (for memory reasons) and you need to restart the microcontroller if a new version is found.

        Returns
        -------
            bool: true if a new version is available, false otherwise
        """
        (current_version, latest_version) = self._check_for_new_version()
        if latest_version > current_version:
            print(f'Updating to version {latest_version}...')
            self._create_new_version_file(latest_version)
            self._download_new_version(latest_version)
            # self._copy_secrets_file()
            self._delete_old_version()
            self._install_new_version()
            return True
        return False

    def _check_for_new_version(self):
        current_version = self.get_version(self.modulepath(self.main_dir))
        latest_version = self.get_latest_version()
        print('Checking version... ')
        print('\tCurrent version: ', current_version)
        print('\tLatest version: ', latest_version)
        return (current_version, latest_version)

    def _create_new_version_file(self, latest_version):
        self.mkdir(self.modulepath(self.new_version_dir))
        with open(self.modulepath(self.new_version_dir + '/.version'), 'w') as versionfile:
            versionfile.write(latest_version)
            versionfile.close()

    def get_version(self, directory, version_file_name='.version'):
        if version_file_name in os.listdir(directory):
            with open(directory + '/' + version_file_name) as f:
                version = f.read()
                return version
        return '0.0'

    def get_latest_version(self):
        latest_release = self.http_client.get(
            f'https://api.github.com/repos/{self.github_repo}/releases/latest')
        gh_json = latest_release.json()
        try:
            version = gh_json['tag_name']
        except KeyError as exc:
            raise ValueError(
                "Release not found: \n",
                "Please ensure release as marked as 'latest', rather than pre-release \n",
                f"github api message: \n {gh_json} \n "
            ) from exc
        latest_release.close()
        return version

    def _download_new_version(self, version):
        print(f'Downloading version {version}')
        self._download_all_files(version)
        print(
            f'Version {version} downloaded to {self.modulepath(self.new_version_dir)}')

    def _download_all_files(self, version, sub_dir=''):
        url = f'https://api.github.com/repos/{self.github_repo}/contents{self.github_src_dir}{self.main_dir}{sub_dir}?ref=refs/tags/{version}'
        gc.collect()
        file_list = self.http_client.get(url)
        file_list_json = file_list.json()
        for file in file_list_json:
            path = self.modulepath(self.new_version_dir + '/' + file['path'].replace(
                self.main_dir + '/', '').replace(self.github_src_dir, ''))
            if file['type'] == 'file':
                gitPath = file['path']
                print('\tDownloading: ', gitPath, 'to', path)
                self._download_file(version, gitPath, path)
            elif file['type'] == 'dir':
                print('Creating dir', path)
                self.mkdir(path)
                self._download_all_files(version, sub_dir + '/' + file['name'])
            gc.collect()

        file_list.close()

    def _download_file(self, version, gitPath, path):
        self.http_client.get(
            f'https://raw.githubusercontent.com/{self.github_repo}/{version}/{gitPath}', saveToFile=path)

    def _delete_old_version(self):
        print(f'Deleting old version at {self.modulepath(self.main_dir)} ...')
        self._rmtree(self.modulepath(self.main_dir))
        print(f'Deleted old version at {self.modulepath(self.main_dir)} ...')

    def _install_new_version(self):
        print(
            f'Installing new version at {self.modulepath(self.main_dir)} ...')
        if self._os_supports_rename():
            os.rename(self.modulepath(self.new_version_dir),
                      self.modulepath(self.main_dir))
        else:
            self._copy_directory(self.modulepath(
                self.new_version_dir), self.modulepath(self.main_dir))
            self._rmtree(self.modulepath(self.new_version_dir))
        print('Update installed, please reboot now')

    def _rmtree(self, directory):
        for entry in os.ilistdir(directory):
            is_dir = entry[1] == 0x4000
            if is_dir:
                self._rmtree(directory + '/' + entry[0])
            else:
                os.remove(directory + '/' + entry[0])
        os.rmdir(directory)

    def _os_supports_rename(self) -> bool:
        self._mk_dirs('otaUpdater/osRenameTest')
        os.rename('otaUpdater', 'otaUpdated')
        result = len(os.listdir('otaUpdated')) > 0
        self._rmtree('otaUpdated')
        return result

    def _copy_directory(self, fromPath, toPath):
        if not self._exists_dir(toPath):
            self._mk_dirs(toPath)

        for entry in os.ilistdir(fromPath):
            is_dir = entry[1] == 0x4000
            if is_dir:
                self._copy_directory(
                    fromPath + '/' + entry[0], toPath + '/' + entry[0])
            else:
                self._copy_file(fromPath + '/' +
                                entry[0], toPath + '/' + entry[0])

    def _copy_file(self, fromPath, toPath):
        with open(fromPath) as fromFile:
            with open(toPath, 'w') as toFile:
                CHUNK_SIZE = 512  # bytes
                data = fromFile.read(CHUNK_SIZE)
                while data:
                    toFile.write(data)
                    data = fromFile.read(CHUNK_SIZE)
            toFile.close()
        fromFile.close()

    def _exists_dir(self, path) -> bool:
        try:
            os.listdir(path)
            return True
        except OSError:
            return False

    def _mk_dirs(self, path: str):
        paths = path.split('/')

        pathToCreate = ''
        for x in paths:
            self.mkdir(pathToCreate + x)
            pathToCreate = pathToCreate + x + '/'

    # different micropython versions act differently when directory already exists
    def mkdir(self, path: str):
        try:
            os.mkdir(path)
        except OSError as exc:
            if exc.args[0] == 17:
                pass

    def modulepath(self, path):
        return self.module + '/' + path if self.module else path
