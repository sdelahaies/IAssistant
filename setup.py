import os
import shutil
import subprocess
import sys
import platform
from pathlib import Path


def get_venv_python():
    return os.path.join("venv", "bin", "python")


def run_in_venv(command):
    venv_python = get_venv_python()
    if isinstance(command, list):
        full_command = [venv_python] + command
    else:
        full_command = [venv_python, "-c", command]

    try:
        subprocess.run(full_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command in virtual environment: {e}")
        sys.exit(1)


def create_virtualenv(force_create=False):
    if not os.path.isdir("venv") or force_create:
        if force_create and os.path.isdir("venv"):
            print("[!] Removing existing virtual environment...")
            shutil.rmtree("venv")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        print("[+] Virtual environment created.")
    else:
        print("[!] Virtual environment already exists.")


def activate_virtualenv():
    activate_script = os.path.join("venv", "bin", "activate")
    # Launches a new bash shell with the virtual environment activated
    subprocess.run(["bash", "-c", f"source {activate_script} && exec $SHELL"])


def install_dependencies(requirements_file):
    python_executable = os.path.join("venv", "bin", "python3")

    command = [
        python_executable,
        "-m",
        "pip",
        "install",
        "-r",
        os.path.join("requirements", requirements_file),
    ]

    try:
        subprocess.check_call(command)
        print(f"[+] Successfully installed dependencies from {requirements_file}.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Error installing dependencies from {requirements_file}: {e}")
        sys.exit(1)


def prLightPurple(skk):
    print("\033[94m {}\033[00m".format(skk))


def install_linux_dependencies():
    package_managers = {
        "apt-get": [
            "sudo",
            "apt-get",
            "install",
            "-y",
            "xclip",
            "ffmpeg",
            "portaudio19-dev",
        ],
        "pacman": ["sudo", "pacman", "-Sy", "xclip", "ffmpeg", "portaudio"],
    }

    for manager, command in package_managers.items():
        try:
            subprocess.check_call(command)
            print(f"[+] Successfully installed dependencies using {manager}")
            prLightPurple("[+] Might be dependencies regarding gtk missing though...")
            return
        except subprocess.CalledProcessError as e:
            print(f"[-] Error installing dependencies using {manager}: {e}")
            continue

    print("[-] Unable to install dependencies. Please install them manually.")
    sys.exit(1)


def copy_file(src, dest):
    """
    Copies a file from the source path to the destination path.
    If the destination file already exists, it prompts the user for confirmation to overwrite.
    """
    if os.path.exists(dest):
        if dest == "config.py":
            should_overwrite = input(
                f"[?] {dest} already exists. Do you want to overwrite it? (y/n): "
            )
        else:
            should_overwrite = input(
                f"[?] {dest} already exists. Do you want to overwrite it? (y/n): "
            )
        if should_overwrite.lower() != "y":
            print(f"[!] Skipping {dest}")
            return
    shutil.copy(src, dest)
    print(f"[+] Copied {src} to {dest}")


def prGreen(skk):
    print("\033[92m {}\033[00m".format(skk))


def create_run_files():
    executable = "run_IAssistant.sh"
    with open(executable, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("source venv/bin/activate\n")
        # f.write("export LD_LIBRARY_PATH=`python3 -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ':' + os.path.dirname(nvidia.cudnn.lib.__file__))'`\n")
        f.write("python3 main.py\n")
    os.chmod(executable, 0o755)

    print(f"[+] Created {prGreen(executable)} run file")


def main():
    print("===== IAssistant Setup =====")
    print()

    if os.path.isdir("venv"):
        user_input = input(
            "[?] A virtual environment already exists. Do you want to create a new one? (y/n): "
        )
        if user_input.lower() == "y":
            create_virtualenv(force_create=True)
        else:
            print("[!] Using existing virtual environment.")
    else:
        create_virtualenv()

    # install dependencies
    install_linux_dependencies()

    # Install the main requirements
    install_dependencies("requirements.txt")
    install_dependencies("gtk_requirements.txt")

    # Ask if the user wants to install extra libraries for faster whisper or transformer whisper
    print("[?] Do you want to install extra libraries for:")
    print("    1. Faster Whisper (local Transcription)")
    print("    2. Transformer Whisper (local Transcription)")
    print("    3. Skip")
    choice = input("[>] Enter your choice (1/2/3): ")

    if choice == "1":
        install_dependencies("faster_whisper_requirements.txt")
    elif choice == "2":
        install_dependencies("transformer_whisper_requirements.txt")
    elif choice == "3":
        print("[!] Skipping installation of extra libraries.")
    else:
        print("[!] Invalid choice. Skipping installation of extra libraries.")

    # Copy config_default.py to config.py
    copy_file("config_default.py", "config.py")

    # Ask if the user wants to install Piper TTS
    install_piper = input("[?] Do you want to install Piper local TTS? (y/n): ")
    if install_piper.lower() == "y":
        script_dir = Path(__file__).parent.resolve()
        command = f"import sys; sys.path.append(r'{script_dir}'); from scripts.installpipertts import setup_piper_tts; setup_piper_tts()"
        run_in_venv(command)
    else:
        print("Piper TTS installation skipped.")

    create_run_files()

    print()
    print("===== Setup Complete =====")

    activate_virtualenv()


if __name__ == "__main__":
    main()
