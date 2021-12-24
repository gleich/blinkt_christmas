import shutil
import os
import sys
import time
from urllib.request import urlopen

tmp_dir = "/home/pi/blinkt_christmas_build"
go_binary_path = os.path.join(tmp_dir, "bin/go")
systemd_service_path = "/etc/systemd/system/blinkt_christmas.service"
blinkt_christmas_bin_path = "/usr/local/bin/blinkt_christmas"


def main() -> None:
    command = sys.argv[1]
    if command == "install":
        setup()
        install_go()
        clone_repo()
        compile()
        install_blinkt_christmas()
        install_blinkt_christmas_service()
        os.chdir("..")
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
    elif command == "uninstall":
        uninstall()
    else:
        print(command, "isn't a valid command")
        exit(1)
    reboot()


def setup() -> None:
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)
    os.chdir(tmp_dir)


def install_go() -> None:
    go_version = "1.17"
    tar_file = f"go{go_version}.linux-armv6l.tar.gz"
    print(f"Installing temporaray version of go {go_version}...")
    command("wget -c https://golang.org/dl/" + tar_file)
    command(f"tar -C {tmp_dir} -xvzf {tar_file}")
    print(f"Setup temporaray version of go {go_version}")


def clone_repo() -> None:
    print("Cloning repo")
    command("git clone https://github.com/gleich/blinkt_christmas.git")
    print("Cloned repo")


def compile() -> None:
    print("Compiling binary from source code:")
    original_gopath = os.getenv("GOPATH")
    os.environ["GOPATH"] = os.path.join(tmp_dir, "goroot")
    os.chdir("blinkt_christmas")
    command("../go/bin/go build -v -o dist/blinkt_christmas .")
    if original_gopath is not None:
        os.environ["GOPATH"] = original_gopath
    os.chdir("..")
    print("Compiled binary")


def install_blinkt_christmas() -> None:
    print("Installing blinkt_christmas at", blinkt_christmas_bin_path)
    if os.path.exists(blinkt_christmas_bin_path):
        os.remove(blinkt_christmas_bin_path)
    os.rename("blinkt_christmas/dist/blinkt_christmas", blinkt_christmas_bin_path)
    print("blinkt_christmas installed at", blinkt_christmas_bin_path)


def install_blinkt_christmas_service() -> None:
    print("Installing systemd service for blinkt_christmas")
    with urlopen(
        "https://raw.githubusercontent.com/gleich/blinkt_christmas/master/blinkt_christmas.service"
    ) as response:
        content = response.read().decode("utf-8")
    with open(systemd_service_path, "w") as systemd_file:
        systemd_file.write(content)
    command("systemctl enable blinkt_christmas")
    print("Added and started systemd service")


def uninstall() -> None:
    os.remove(blinkt_christmas_bin_path)
    print("Deleted binary")
    command("systemctl disable blinkt_christmas")
    print("Disabled systemd service")
    os.remove(systemd_service_path)
    print("Deleted systemd service file")


def reboot() -> None:
    print(
        "\nRebooting pi in 3 seconds. You might need to cut the power to fully turn off the lights."
    )
    for i in reversed(range(2)):
        print(i + 1)
        time.sleep(1)
    print("Rebooting now")
    command("reboot")


def command(cmd: str) -> None:
    """Run os.system but exit with a failure if the exit code is not zero

    Args:
        cmd (str): Command to run
    """
    code = os.system(cmd)
    if code != 0:
        print(f"Failed to run {cmd} with status code of {code}")
        exit(1)


if __name__ == "__main__":
    main()
