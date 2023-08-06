import json

import fabricio

from . import Image


class Container(object):

    image = None  # type: Image

    cmd = None

    user = None

    ports = None

    env = None

    volumes = None

    links = None

    hosts = None

    network = None

    restart_policy = None

    stop_signal = None

    stop_timeout = 10

    def __init__(self, name, options=None):
        self.name = name
        self.options = options or {}

    def __str__(self):
        return str(self.name)

    def fork(self, name=None, options=None):
        if name is None:
            name = self.name
        if options is None:
            options = self.options.copy()
        return self.__class__(name=name, options=options)

    def __copy__(self):
        return self.fork()

    @property
    def info(self):
        command = 'docker inspect --type container {container}'
        info = fabricio.run(command.format(container=self))
        return json.loads(info)[0]

    def delete(self, force=False, ignore_errors=False):
        command = 'docker rm {force}{container}'
        force = force and '--force ' or ''
        fabricio.run(
            command.format(container=self, force=force),
            ignore_errors=ignore_errors,
        )

    def run(self, tag=None, registry=None):
        self.__class__.image[registry:tag].run(
            cmd=self.cmd,
            temporary=False,
            name=self.name,
            user=self.user,
            ports=self.ports,
            env=self.env,
            volumes=self.volumes,
            links=self.links,
            hosts=self.hosts,
            network=self.network,
            restart_policy=self.restart_policy,
            stop_signal=self.stop_signal,
            options=self.options,
        )

    def execute(self, cmd, ignore_errors=False, quiet=True):
        command = 'docker exec --tty --interactive {container} {cmd}'
        return fabricio.run(
            command.format(container=self, cmd=cmd),
            ignore_errors=ignore_errors,
            quiet=quiet,
        )

    def start(self):
        command = 'docker start {container}'
        fabricio.run(command.format(container=self))

    def stop(self, timeout=None):
        if timeout is None:
            timeout = self.stop_timeout
        command = 'docker stop --time {timeout} {container}'
        fabricio.run(command.format(container=self, timeout=timeout))

    def restart(self, timeout=None):
        if timeout is None:
            timeout = self.stop_timeout
        command = 'docker restart --time {timeout} {container}'
        fabricio.run(command.format(container=self, timeout=timeout))

    def rename(self, new_name):
        command = 'docker rename {container} {new_name}'
        fabricio.run(command.format(container=self, new_name=new_name))
        self.name = new_name

    def signal(self, signal):
        command = 'docker kill --signal {signal} {container}'
        fabricio.run(command.format(container=self, signal=signal))

    def update(self, tag=None, registry=None, force=False):
        if not force:
            try:
                current_image_id = self.image.id
            except RuntimeError:  # current container not found
                pass
            else:
                new_image = self.__class__.image[registry:tag]
                if current_image_id == new_image.id:
                    fabricio.log('No change detected, update skipped.')
                    self.start()  # force starting container
                    return False
        new_container = self.fork(name=self.name)
        obsolete_container = self.get_backup_container()
        try:
            obsolete_image = obsolete_container.image
        except RuntimeError:
            pass
        else:
            obsolete_container.delete()
            obsolete_image.delete(ignore_errors=True)
        try:
            backup_container = self.fork()
            backup_container.rename(obsolete_container.name)
        except RuntimeError:
            pass
        else:
            backup_container.stop()
        new_container.run(tag=tag, registry=registry)
        return True

    def revert(self):
        failed_image = self.image
        self.stop()
        self.delete()
        failed_image.delete(ignore_errors=True)
        backup_container = self.get_backup_container()
        backup_container.start()
        backup_container.rename(self.name)

    def get_backup_container(self):
        return self.fork(name='{container}_backup'.format(container=self))

    def migrate(self, tag=None, registry=None):
        pass

    def migrate_back(self):
        pass

    def backup(self):
        pass

    def restore(self, backup_name=None):
        pass
