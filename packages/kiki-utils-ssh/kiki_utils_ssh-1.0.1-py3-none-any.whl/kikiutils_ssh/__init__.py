import asyncssh


class AsyncSSHClient:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        known_hosts=None
    ):
        self.c: asyncssh.SSHClientConnection
        self.s: asyncssh.SFTPClient

        self.host = host
        self.known_hosts = known_hosts
        self.password = password
        self.port = port
        self.username = username

    async def connect(self, **kwargs):
        """Connect to server and open sftp connection.

        If the connection error, return error Exception.

        @param `kwargs` - `asyncssh.connect` other parameters.
        """

        try:
            self.c = await asyncssh.connect(
                self.host,
                self.port,
                known_hosts=self.known_hosts,
                password=self.password,
                username=self.username,
                **kwargs
            )

            self.s = await self.c.start_sftp_client()
        except Exception as error:
            return error

    async def chdir(self, remotepath: str):
        """Change sftp directory."""

        await self.s.chdir(remotepath)

    def close(self):
        """Close sftp and ssh connection."""

        self.s.exit()
        self.c.close()

    async def get_os_info(self):
        """Get os version and id, only work on linux."""

        result = await self.run('''
            echo $(grep "^ID=" /etc/os-release | cut -d'=' -f2 | tr -d '"')
            echo $(grep "^VERSION_ID=" /etc/os-release | cut -d'=' -f2 | tr -d '"')
        ''')

        return result.strip().split('\n')

    async def isdir(self, path: str):
        """Check remotepath is dir."""

        return await self.s.isdir(path)

    async def isfile(self, path: str):
        """Check remotepath is file."""

        return await self.s.isfile(path)

    async def mkdir(self, remotepath: str, **kwargs):
        """Make remote directory."""

        await self.s.mkdir(remotepath, **kwargs)

    async def mkdirs(
        self,
        remotepath: str,
        exist_ok: bool = True,
        **kwargs
    ):
        """Make remote directories."""

        await self.s.makedirs(remotepath, exist_ok=exist_ok, **kwargs)

    async def putdir(self, localpath: str, remotepath: str, **kwargs):
        """Upload dir."""

        await self.putfile(localpath, remotepath, recurse=True, **kwargs)

    async def putfile(self, localpath: str, remotepath: str, **kwargs):
        """Upload file."""

        await self.s.put(localpath, remotepath, **kwargs)

    async def rm(self, remotepath: str):
        """Remove remote file."""

        await self.s.remove(remotepath)

    async def rmdir(self, remotepath: str):
        """Remove remote dir."""

        await self.s.rmdir(remotepath)

    async def rmtree(self, remotepath: str, **kwargs):
        """Force remove remote dir.

        @param `kwargs` - sftp rmtree other parameters.
        """

        await self.s.rmtree(remotepath, **kwargs)

    async def run(
        self,
        command: str,
        get_std_out: bool = True,
        **kwargs
    ):
        """Run command and return stdout or `SSHCompletedProcess`."""

        result = await self.c.run(command, **kwargs)

        if get_std_out:
            return str(result.stdout)

        return result

    async def run_and_show(
        self,
        command: str,
        **kwargs
    ):
        """Run command and instant display result, then return all result."""

        results = ''
        process = await self.c.create_process(
            command,
            **kwargs
        )

        async for line in process.stdout:
            results += str(line)
            print(line, end='')

        return results
