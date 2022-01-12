import os
import subprocess
import sys


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def command(cmd):
    return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()


def print_color(txt, color=""):
    print(f"{color}{txt}{bcolors.ENDC}")


def input_wrap(txt):
    return input(txt).strip().lower()


if __name__ == "__main__":
    print_color(
        """==============================================
Aiffel SSH@Git setting helper
==============================================
1. 아이펠 서버 환경에서 Git을 SSH로 사용할 수 있도록 키를 생성합니다.
2. ls -al 명령어를 명령어 ll 로 줄여줍니다.

실행 중 종료하고 싶으시면 언제든 Ctrl + C 를 누르시면 됩니다!   
""",
        bcolors.OKGREEN,
    )

    now_pwd = command("pwd")
    print(f"현재 디렉토리 위치: {now_pwd}")
    print("")

    if now_pwd != "/aiffel/aiffel":
        print_color(
            "아이펠 서버 환경이 아닌 것 같습니다..\n아래 URL을 참고하세요\nhttps://~~~", bcolors.WARNING
        )

    if not os.path.isfile("bash_shortcut.sh"):
        command(
            "wget https://raw.githubusercontent.com/andy-kwon/aiffel-exams/master/helper/bash_shortcut.sh"
        )

    command("bash bash_shortcut.sh")

    if os.path.isfile(f"/root/.ssh/id_rsa"):
        print_color(f"===============================")
        print_color(command(f"cat /root/.ssh/id_rsa.pub"), bcolors.OKGREEN)
        print_color(f"===============================")
        print_color(
            f"ssh 접속키가 세팅되어 있습니다. Github에 키를 설정하셨으면 다시 하실 필요 없습니다..", bcolors.OKCYAN
        )
        print_color(f"프로그램을 종료합니다", bcolors.WARNING)
        sys.exit()

    ssh_dir = f"{now_pwd}/.ssh"
    print("")
    if not os.path.isdir(ssh_dir):
        print_color("Step 1. .ssh 폴더를 찾을 수 없습니다.", bcolors.OKCYAN)
        print_color(f"> .ssh 폴더를 생성합니다: {ssh_dir}", bcolors.OKCYAN)
        command(f"mkdir -p {ssh_dir}")
    else:
        print_color(f"Step 1. 이미 생성한 .ssh 폴더가 있습니다: {ssh_dir}", bcolors.OKCYAN)

    rsa_path = f"{ssh_dir}/id_rsa"
    if os.path.isfile(rsa_path):
        print("")
        print_color("Step 2. ssh 키파일이 존재합니다. 다음으로 계속 진행합니다", bcolors.OKCYAN)

    else:
        print("")
        print_color("Step 2. ssh 키파일이 존재하지 않습니다", bcolors.OKCYAN)
        print_color("> ssh 키파일을 생성합니다.", bcolors.OKCYAN)
        print_color(
            "> 1. [Enter passphrase (empty for no passphrase)] 문구가 뜨면 엔터를 누르세요",
            bcolors.OKCYAN,
        )
        print_color(
            "> 2. [Enter same passphrase again] 문구가 뜨면 엔터를 누르세요", bcolors.OKCYAN
        )

        command(f"ssh-keygen -f {rsa_path}")

    if not os.path.isfile(rsa_path):
        print_color(f"생성된 키파일을 찾을 수 없습니다.. 문제가 계속되면 문의해주세요 @권형주", bcolors.FAIL)
        sys.exit()

    print("")
    print_color(f"Step 3. ssh 키파일을 성공적으로 생성했습니다: {rsa_path}", bcolors.OKCYAN)
    print_color(f"===============================")
    print_color(command(f"cat {rsa_path}.pub"), bcolors.OKGREEN)
    print_color(f"===============================")
    print_color(f"> 1. 위 초록색 글씨를 쭉- 드래그하면 복사가 됩니다.", bcolors.OKCYAN)
    print_color(f"> 2. 아래 URL로 접속하고 우측 상단의 [NEW SSH Key] 버튼을 클릭하세요", bcolors.OKCYAN)
    print_color(f"> URL: https://github.com/settings/keys", bcolors.OKCYAN)
    print_color(f"> 3. [Title] 에 이 키를 식별할 수 있는 값을 넣어주세요.", bcolors.OKCYAN)
    print_color(f"> 예) aiffel@lms", bcolors.OKCYAN)
    print_color(f"> 4. [Key] 에 복사한 값을 붙여 넣고 저장하세요.", bcolors.OKCYAN)

    print("")
    print_color(f"> 파일 권한을 조정하고 폴더 위치를 재 조정합니다", bcolors.OKCYAN)
    command(f"chmod 0400 {rsa_path}")
    command(f"cp -R {ssh_dir} /root")

    print("")
    print_color(f"> 간단한 명령어들을 추가합니다", bcolors.OKCYAN)
    command(f'touch ~/.bashrc && echo ""')
    print_color(f"이제 세팅이 마무리 되었습니다!", bcolors.OKGREEN)