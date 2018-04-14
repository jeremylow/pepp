import pip


installer = pip.commands.InstallCommand()
install_args = installer.parse_args(["--quiet"])[0]

dler = pip.commands.DownloadCommand()
dler_args = dler.parse_args([])[0]

if __name__ == "__main__":
    ret = installer.run(install_args, ["attrs"])
