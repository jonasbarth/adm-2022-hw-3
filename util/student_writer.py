import os


def write_students(students, path):
    """Writes an iterable of students to a file at the given path."""
    if not os.path.isdir(path):
        raise OSError(f'The provided path: {path} does not exist.')

    file_name = f'{path}/RankingList.txt'

    with open(file_name, 'w') as file:
        for student in students:
            file.write(f'{str(student)}\n')