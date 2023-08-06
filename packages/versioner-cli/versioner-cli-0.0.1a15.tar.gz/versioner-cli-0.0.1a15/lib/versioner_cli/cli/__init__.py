from future import standard_library
standard_library.install_aliases()
import logging
from subprocess import getoutput, getstatusoutput, CalledProcessError, PIPE
PYTHON2 = False
try:
    from subprocess import run
except ImportError:
    logging.getLogger(__name__).info('running python2')
    PYTHON2 = True
from os import environ
from docker import Client
from docker.errors import APIError
import requests
from requests.auth import HTTPBasicAuth
from future.utils import raise_with_traceback


logger = logging.getLogger(__name__)


class VersionerCli(object):
    DEFAULT_CONFIG_PATH = '/etc/default/versioner'
    pre_tasks = []
    build_tasks = []
    post_tasks = []

    @staticmethod
    def continuous_deployment_hook(username, password, url):
        """

        :param username:
        :param password:
        :param url:
        :return:
        """
        if requests.post(url, auth=HTTPBasicAuth(username=username, password=password)).status_code == 200:
            return True
        return False

    def tag_docker(self, image, version, repo):
        """

        :param image:
        :param version:
        :param repo:
        :return:
        """
        success = self.docker.tag(image=image, tag=version, repository=repo)
        if success:
            response = [line for line in self.docker.push(repo, tag=version, stream=True, auth_config=self.docker_auth)]
            if 'error' in ''.join(response):
                raise_with_traceback(APIError('Something went wrong pushing to dockerhub'))
            return True

    @staticmethod
    def npm_version(version):
        """

        :param version:
        :return:
        """
        try:
            logger.info('running npm version')
            if not PYTHON2:
                output = run(["npm", "version", version],
                             shell=True,
                             check=True,
                             universal_newlines=True,
                             stdout=PIPE)
            else:
                output = getoutput(["npm", "version", version]).rstrip('\n')
            logger.info('output: {}'.format(output.stdout))
        except CalledProcessError as msg:
            logger.error(msg)

    @staticmethod
    def npm_publish(tag):
        """

        :param tag:
        :return:
        """
        try:
            logger.info('running npm publish --tag {}'.format(tag))
            if not PYTHON2:
                output = run(["npm", "publish", "--tag", tag],
                             shell=True,
                             check=True,
                             universal_newlines=True,
                             stdout=PIPE)
            else:
                output = getoutput(["npm", "publish", "--tag", tag]).rstrip('\n')
            logger.info('output: {}'.format(output.stdout))
        except CalledProcessError as msg:
            logger.error(msg)

    @staticmethod
    def git_push_flags(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        try:
            logger.info('running npm publish --follow-flags')
            if not PYTHON2:
                output = run(["git", "push", "--follow-flags"], shell=True, check=True, universal_newlines=True, stdout=PIPE)
            else:
                output = getoutput(["git", "push", "--follow-flags"]).rstrip('\n')
            logger.info('output: {}'.format(output.stdout))
        except CalledProcessError as msg:
            logger.error(msg)

    def setup(self):
        """

        :return:
        """
        docker_user = environ.get('DOCKER_USER')
        docker_pass = environ.get('DOCKER_PASS')
        docker_email = environ.get('DOCKER_EMAIL')
        if None in [docker_email, docker_pass, docker_user]:
            logger.error('Environment Variable not set')
            raise_with_traceback(LookupError('Environment Variable not set'))
        self.docker = Client(base_url='unix://var/run/docker.sock')
        try:
            self.docker_auth = self.docker.login(username=docker_user,
                                                 password=docker_pass,
                                                 email=docker_email)
        except APIError as msg:
            logger.error(msg)

    def __init__(self):
        self.docker = None
        self.docker_auth = {}
        self.setup()
