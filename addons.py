import sys, os, shutil, errno
from pathlib import Path

def ig_f(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]

def enable_addon(addon_name):
    
    working_dir = Path(os.getcwd())
    addons_dir = Path.joinpath(working_dir, 'addons')
    game_dir = Path.joinpath(working_dir, 'game')

    target = Path(game_dir)
    symlinks=False

    active_addons_file = os.path.abspath(addons_dir) + "\\active_addons.txt"
    
    try:
        if Path.is_dir(Path.joinpath(addons_dir, addon_name)):
            addon_src = Path.joinpath(addons_dir, addon_name)
        else:
            print(f'Error: addon {addon_name} not found')
            return
    except Exception as e:
        print(f'Error: {e}')
        return


    if game_dir.exists():
        print("game dir exists")
    if addons_dir.exists():
        print("addon dir exists")
    else:
        print("addon directory does not exist")
        print(f"creating directory \"{addons_dir}\"")

        os.mkdir(addons_dir)

    try:
        with open(active_addons_file, 'r') as file:
            file.seek(0)
            if addon_name in file.read():
                print(f"addon '{addon_name}' already enabled")
                return
    except Exception as e:
        print(f'Error: {e}')


    #Create directory structure
    for dir in os.listdir(addon_src):
        file_source = Path.joinpath(addon_src, dir)
        file_target = Path.joinpath(target, dir)
        if os.path.isdir(file_source):
            shutil.copytree(file_source, file_target, symlinks, dirs_exist_ok=True, ignore=ig_f)

    #Copy files
    for root, dirs, files in os.walk(addon_src, topdown=True):
        #print(os.path.basename(root))
        relative_path = os.path.relpath(root, addon_src)
        file_target = Path.joinpath(target, relative_path)

        for file in files:
            shutil.copy2(os.path.join(root, file), os.path.join(file_target, file))
            print(f"copying {file} to {file_target}...")

    try:
        with open(active_addons_file, 'a') as file:
            file.write(addon_name + '\n')
            print(f"'{addon_name}' added to {os.path.relpath(active_addons_file, addons_dir)}")
    except Exception as e:
        print(f'Error: {e}')

def disable_addon(addon_name):
    
    working_dir = Path(os.getcwd())
    addons_dir = Path.joinpath(working_dir, 'addons')
    game_dir = Path.joinpath(working_dir, 'game')

    target = Path(game_dir)
    symlinks=False

    active_addons_file = os.path.abspath(addons_dir) + "\\active_addons.txt"

    file_list = []
    active_addons_list = []

    try:
        if Path.is_dir(Path.joinpath(addons_dir, addon_name)):
            addon_src = Path.joinpath(addons_dir, addon_name)
        else:
            print(f'Error: addon {addon_name} not found')
            return
    except Exception as e:
        print(f'Error: {e}')
        return

    try:
        with open(active_addons_file, "r") as input:
            temp = os.path.abspath(addons_dir) + "\\temp.txt"

            if addon_name.strip("\n") in input.read():
                input.seek(0)
                with open(temp, "w") as output:
                    for line in input:
                        if line.strip("\n") != addon_name:
                            output.write(line)
                shutil.move(temp, active_addons_file)
            else:
                print(f"addon '{addon_name}' already disabled or not found")
                return
    except Exception as e:
        print(f'Error: {e}')


    for root, dirs, files in os.walk(addon_src, topdown=True):
        #print(os.path.basename(root))
        relative_path = os.path.relpath(root, addon_src)
        file_target = Path.joinpath(target, relative_path)

        for file in files:
            file_list.append(file)
    
    

    for root, dirs, files in os.walk(game_dir, topdown=False):
        for file in files:
            if file in file_list:
                os.remove(os.path.join(root, file))
                print(f"removing file {file}...")


        for dir in dirs:
            current_dir = os.path.join(root, dir)
            empty = os.listdir(current_dir)
            if len(empty) == 0:
                Path.rmdir(current_dir)
                print(f"removed directory {current_dir}...")


if __name__ == "__main__":
    addon_name = 'coolmod'
    #addon_name = 'evilmansion_fixed'
    #addon_name = 'dummyaddon'
    #enable_addon(addon_name)
    disable_addon(addon_name)