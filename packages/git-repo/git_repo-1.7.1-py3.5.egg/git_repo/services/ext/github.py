#!/usr/bin/env python

import logging
log = logging.getLogger('git_repo.github')

from ..service import register_target, RepositoryService, os
from ...exceptions import ResourceError, ResourceExistsError, ResourceNotFoundError

import github3

from git.exc import GitCommandError

@register_target('hub', 'github')
class GithubService(RepositoryService):
    fqdn = 'github.com'

    def __init__(self, *args, **kwarg):
        self.gh = github3.GitHub()
        super(GithubService, self).__init__(*args, **kwarg)

    def connect(self):
        try:
            self.gh.login(token=self._privatekey)
            self.username = self.gh.user().name
        except github3.models.GitHubError as err:
            if err.code is 401:
                if not self._privatekey:
                    raise ConnectionError('Could not connect to Github. '
                                          'Please configure .gitconfig '
                                          'with your github private key.') from err
                else:
                    raise ConnectionError('Could not connect to Github. '
                                          'Check your configuration and try again.') from err

    def create(self, user, repo, add=False):
        if user != self.username:
            raise NotImplementedError("Project creation supported for authentified user only!")
        try:
            self.gh.create_repo(repo)
        except github3.models.GitHubError as err:
            if err.code == 422 or err.message == 'name already exists on this account':
                raise ResourceExistsError("Project already exists.") from err
            else: # pragma: no cover
                raise ResourceError("Unhandled error.") from err
        if add:
            self.add(user=self.username, repo=repo, tracking=self.name)

    def fork(self, user, repo, branch='master', clone=False):
        log.info("Forking repository {}/{}…".format(user, repo))
        # checking for an 'upstream' remote.
        upstream_remotes = list(filter(lambda x: x.name == 'upstream', self.repository.remotes))
        if len(upstream_remotes) != 0:
            raise ResourceExistsError('A remote named `upstream` already exists. Has this repo already been forked?')
        # forking the repository on the service
        try:
            fork = self.gh.repository(user, repo).create_fork()
        except github3.models.GitHubError as err:
            if err.message == 'name already exists on this account':
                raise ResourceExistsError("Project already exists.") from err
            else: # pragma: no cover
                raise ResourceError("Unhandled error: {}".format(err)) from err
        # checking if a remote with the service's name already exists
        service_remotes = list(filter(lambda x: x.name == self.name, self.repository.remotes))
        if len(service_remotes) != 0:
            # if it does, rename it to upstream
            repo.delete(service_remotes[0])
            repo.create_remote('upstream', service_remotes[0].url)
        else:
            # otherwise create an upstream remote with the source repository
            self.add(user=user, repo=repo, name='upstream', alone=True)
        # add the service named repository
        remote = self.add(repo=repo, user=self.username, tracking=self.name)
        if clone:
            self.pull(remote, branch)
        log.info("New forked repository available at {}/{}".format(self.url_ro,
                                                                   fork.full_name))

    def delete(self, repo, user=None):
        if not user:
            user = self.username
        try:
            repository = self.gh.repository(user, repo)
            if repository:
                result = repository.delete()
            if not repository or not result:
                raise ResourceNotFoundError('Cannot delete: repository {}/{} does not exists.'.format(user, repo))
        except github3.models.GitHubError as err: # pragma: no cover
            if err.code == 403:
                raise ResourcePermissionError('You don\'t have enough permissions for deleting the repository. '
                                              'Check the namespace or the private token\'s privileges') from err
            raise ResourceError('Unhandled exception: {}'.format(err)) from err

    def get_repository(self, user, repo):
        repository = self.gh.repository(user, repo)
        if not repository:
            raise ResourceNotFoundError('Cannot delete: repository {}/{} does not exists.'.format(user, repo))
        return repository

    def _format_gist(self, gist):
        return gist.split('https://gist.github.com/')[-1].split('.git')[0]

    def gist_list(self, gist=None):
        if not gist:
            for gist in self.gh.iter_gists(self.gh.user().name):
                yield (gist.html_url, gist.description)
        else:
            gist = self.gh.gist(self._format_gist(gist))
            if gist is None:
                raise ResourceNotFoundError('Gist does not exists.')
            for gist_file in gist.iter_files():
                yield (gist_file.language if gist_file.language else 'Raw text',
                        gist_file.size,
                        gist_file.filename)


    def gist_fetch(self, gist, fname=None):
        try:
            gist = self.gh.gist(self._format_gist(gist))
        except Exception as err:
            raise ResourceNotFoundError('Could not find gist') from err
        if gist.files == 1 and not fname:
            gist_file = list(gist.iter_files())[0]
        else:
            for gist_file in gist.iter_files():
                if gist_file.filename == fname:
                    break
            else:
                raise ResourceNotFoundError('Could not find file within gist.')

        return gist_file.content

    def gist_clone(self, gist):
        try:
            gist = self.gh.gist(gist.split('https://gist.github.com/')[-1])
        except Exception as err:
            raise ResourceNotFoundError('Could not find gist') from err
        remote = self.repository.create_remote('gist', gist.git_push_url)
        self.pull(remote, 'master')

    def gist_create(self, gist_pathes, description, secret=False):
        def load_file(fname, path='.'):
            with open(os.path.join(path, fname), 'r') as f:
                return {'content': f.read()}

        gist_files = dict()
        for gist_path in gist_pathes:
            if not os.path.isdir(gist_path):
                gist_files[os.path.basename(gist_path)] = load_file(gist_path)
            else:
                for gist_file in os.listdir(gist_path):
                    if not os.path.isdir(os.path.join(gist_path, gist_file)) and not gist_file.startswith('.'):
                        gist_files[gist_file] = load_file(gist_file, gist_path)

        gist = self.gh.create_gist(
                description=description,
                files=gist_files,
                public=not secret # isn't it obvious? ☺
            )

        return gist.html_url

    def gist_delete(self, gist_id):
        gist = self.gh.gist(self._format_gist(gist_id))
        if not gist:
            raise ResourceNotFoundError('Could not find gist')
        gist.delete()

    def request_create(self, user, repo, local_branch, remote_branch, title, description=None):
        repository = self.gh.repository(user, repo)
        if not repository:
            raise ResourceNotFoundError('Could not find repository `{}/{}`!'.format(user, repo))
        if not local_branch:
            remote_branch = self.repository.active_branch.name or self.repository.active_branch.name
        if not remote_branch:
            local_branch = repository.master_branch or 'master'
        try:
            request = repository.create_pull(title,
                    base=local_branch,
                    head=':'.join([user, remote_branch]),
                    body=description)
        except github3.models.GitHubError as err:
            if err.code == 422:
                for error in err.errors:
                    if 'message' in error:
                        if 'No commits' in error['message']:
                            raise ResourceError(error['message'])
                else:
                    if 'message' in error:
                        raise ResourceError(error['message'])
                raise ResourceError("Unhandled formatting error: {}".format(err.errors))


        return {'local': local_branch, 'remote': remote_branch, 'ref': request.number}

    def request_list(self, user, repo):
        repository = self.gh.repository(user, repo)
        for pull in repository.iter_pulls():
            yield ( str(pull.number), pull.title, pull.links['issue'] )

    def request_fetch(self, user, repo, request, pull=False):
        if pull:
            raise NotImplementedError('Pull operation on requests for merge are not yet supported')
        try:
            for remote in self.repository.remotes:
                if remote.name == self.name:
                    local_branch_name = 'request/{}'.format(request)
                    self.fetch(
                        remote,
                        'pull/{}/head'.format(request),
                        local_branch_name
                    )
                    return local_branch_name
            else:
                raise ResourceNotFoundError('Could not find remote {}'.format(self.name))
        except GitCommandError as err:
            if 'Error when fetching: fatal: Couldn\'t find remote ref' in err.command[0]:
                raise ResourceNotFoundError('Could not find opened request #{}'.format(request)) from err
            raise err

    @classmethod
    def get_auth_token(cls, login, password):
        import platform
        auth = github3.GitHub().authorize(login, password,
                scopes=[ 'repo', 'delete_repo', 'gist' ],
                note='git-repo token used on {}'.format(platform.node()),
                note_url='https://github.com/guyzmo/git-repo')
        return auth.token

    @property
    def user(self):
        return self.gh.user().name

