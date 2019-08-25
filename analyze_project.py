# -- imports --
import distutils.dir_util
import os
import shutil
import stat
import subprocess

from git import InvalidGitRepositoryError
from pydriller import RepositoryMining


def _get_all_commits(folder_path):
    if not os.path.exists(folder_path):
        print("Folder doesn't exist: " + folder_path)
        return
    os.chdir(folder_path)
    versions = []
    try:
        for commit in RepositoryMining(folder_path).traverse_commits():
            versions.append((commit.hash, commit.committer_date))
    except InvalidGitRepositoryError as error:
        print(error)
    return versions


def _get_selected_commits(folder_path, max_versions_to_analyze):
    versions = _get_all_commits(folder_path)
    if len(versions) <= max_versions_to_analyze:
        return versions
    selected_versions = []
    interval = int((len(versions) - 1) / (max_versions_to_analyze - 1))
    for i in range(max_versions_to_analyze):
        selected_versions.append(versions[i * interval])
        # print(versions[i * interval][0] + ": " + str(versions[i * interval][1].date()))
    return selected_versions


def _switch_to_commit(folder_path, version):
    print("Switching to version " + version)
    os.chdir(folder_path)
    result = subprocess.check_output(["git", "checkout", "-f", "-b", version[len(version) - 5:], version])
    print(result)


def _delete_temp_folder(trend_temp_folder):
    print("Deleting " + trend_temp_folder)
    if not os.path.exists(trend_temp_folder):
        return
    for dirName, subdirList, fileList in os.walk(trend_temp_folder):
        for fname in fileList:
            os.chmod(os.path.join(dirName, fname), stat.S_IWRITE)
    try:
        shutil.rmtree(trend_temp_folder)
    except Exception as exception:
        print('Error while deleting temp folder')
        print(exception)
        exit(1)


def _create_temp_folder(trend_temp_folder):
    try:
        if not os.path.exists(trend_temp_folder):
            os.makedirs(trend_temp_folder)
    except Exception as exception:
        print('Error while creating temp folder')
        print(exception)
        exit(2)


def _copy_folder(src_folder, dest_folder):
    print("Copying {0} to temp folder".format(src_folder))
    try:
        distutils.dir_util.copy_tree(src_folder, dest_folder)
    except Exception as ex:
        print('Error while copying repository to temp folder: ' + str(ex))
        exit(3)


def _analyze(source_folder, out_folder, designitejava_path):
    if os.path.exists(out_folder):
        return # the version is already analyzed
    os.makedirs(out_folder)
    # -Xmx argument value depends on the size of your source code.
    subprocess.call(["java", "-Xmx4096m", "-jar", designitejava_path, "-i", source_folder, "-o", out_folder])


def _build_project(temp_folder_path):
    # We need to build the project to have class files.
    # These class files are important for correct symbol resolution
    subprocess.call(['mvn', 'clean', 'install', '-DskipTests'])


def analyze_multiple_versions(repo_source_folder,
                              result_folder_base,
                              temp_folder_path,
                              max_versions_to_analyze,
                              designitejava_path):
    _delete_temp_folder(temp_folder_path)
    _create_temp_folder(temp_folder_path)
    _copy_folder(repo_source_folder, temp_folder_path)
    versions = _get_selected_commits(repo_source_folder, max_versions_to_analyze)
    for version in versions:
        print("Processing version " + version[0])
        _switch_to_commit(temp_folder_path, version[0])
        _build_project(temp_folder_path)
        _analyze(temp_folder_path, os.path.join(result_folder_base, version[0]), designitejava_path)
    print("Done")
    return versions



