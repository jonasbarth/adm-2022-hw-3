from domain import Student


def parse_students_from(path):
    """Parses students from a file at the provided path."""
    students = []
    with open(path, 'r') as file:
        n_applications, n_exams = map(int, file.readline().split())

        for _ in range(n_applications):
            student_info = file.readline().split()

            student_name = ' '.join(student_info[:len(student_info) - n_exams])
            student_marks = list(map(int, student_info[len(student_info) - n_exams:]))

            student = Student(student_name, student_marks)
            students.append(student)

    return students
