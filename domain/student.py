from functools import reduce


class Student:
    """Represents a student.

    Attributes
    ----------
    name : str
        full name of the student.
    grades : []
        a list of grades that the student obtained.
    """

    def __init__(self, name, grades):
        self.name = name
        self.grades = grades
        self.avg_grade_computed = False
        self.avg_grade = -1

    def get_avg_grade(self):
        """Gets the average grade of the student."""
        if self.avg_grade_computed:
            return self.avg_grade

        total = reduce(lambda a, b: a + b, self.grades)

        self.avg_grade = round(total / len(self.grades), 2)
        self.avg_grade_computed = True
        return self.avg_grade

    def __lt__(self, other):
        if self.get_avg_grade() == other.get_avg_grade():
            return self.name > other.name

        return self.get_avg_grade() < other.get_avg_grade()

    def __le__(self, other):
        if self.get_avg_grade() == other.get_avg_grade():
            return self.name >= other.name

        return self.get_avg_grade() <= other.get_avg_grade()

    def __gt__(self, other):
        if self.get_avg_grade() == other.get_avg_grade():
            return self.name < other.name

        return self.get_avg_grade() > other.get_avg_grade()

    def __ge__(self, other):
        if self.get_avg_grade() == other.get_avg_grade():
            return self.name <= other.name

        return self.get_avg_grade() >= other.get_avg_grade()

    def __eq__(self, other):
        return self.get_avg_grade() == other.get_avg_grade()

    def __repr__(self):
        return f'{self.name} {self.get_avg_grade()}'

    def __str__(self):
        return self.__repr__()
