import os

RESOURCE_PATH = '../resources'


def resource_files(starts_with: str, ends_with: str) -> []:
    file_list = []
    for file in os.listdir(RESOURCE_PATH):
        if file.startswith(starts_with) and file.endswith(ends_with):
            file_list.append(file.replace(ends_with, ''))
    return file_list
