class Person:
    def __init__(self, name, age, gender, phone):
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone

    def get_details(self):
        return f"{self.name} ({self.gender}) aged {self.age}, phone: {self.phone}"


class Student(Person):
    def __init__(self, name, age, gender, phone, rollno):
        super().__init__(name, age, gender, phone)
        self.rollno = rollno
        self.marks = {}

    def get_details(self):
        return f"{self.name} ({self.gender}) aged {self.age}, Roll No: {self.rollno}, phone: {self.phone}"

    def add_marks(self, subject, score):
        self.marks[subject] = score

    def get_marks(self, subject):
        return self.marks[subject]


class Teacher(Person):
    def __init__(self, name, age, gender, phone, course):
        super().__init__(name, age, gender, phone)
        self.course = course
        self.students = {}

    def get_details(self):
        return f"{self.name} ({self.gender}) aged {self.age}, phone: {self.phone}, Course: {self.course}"

    def add_student(self, student):
        self.students[student.rollno] = student

    def get_student(self, rollno):
        return self.students[rollno]

    def average_marks(self):
        if len(self.students) == 0:
            return 0
        total = sum([sum(student.marks.values()) for student in self.students.values()])
        return total / len(self.students)

class School:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.teachers = []
        self.students = []

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def add_student(self, student):
        self.students.append(student)

    def remove_teacher(self, teacher):
        self.teachers.remove(teacher)

    def remove_student(self, student):
        self.students.remove(student)
    def get_all_students(self):
        return self.students
def test_system():
    # 创建学校
    school = School("ABC School", "Somewhere, USA")

    # 添加老师
    teacher1 = Teacher("John Smith", 35, "M", "555-1234", "Mathematics")
    teacher2 = Teacher("Jane Doe", 30, "F", "555-5678", "Science")
    school.add_teacher(teacher1)
    school.add_teacher(teacher2)

    # 添加学生
    student1 = Student("Alice", 15, "F", "555-1111", "1001")
    student2 = Student("Bob", 16, "M", "555-2222", "1002")
    student3 = Student("Charlie", 17, "M", "555-3333", "1003")
    school.add_student(student1)
    school.add_student(student2)
    school.add_student(student3)

    # 添加学生成绩
    student1.add_marks("Mathematics", 90)
    student1.add_marks("Science", 80)
    student2.add_marks("Mathematics", 75)
    student2.add_marks("Science", 85)
    student3.add_marks("Mathematics", 95)
    student3.add_marks("Science", 90)

    # 查询学生信息
    print("Student Details:")
    for student in school.get_all_students():
        print("- ", student.get_details())
        for subject, score in student.marks.items():
            print(f"  {subject}: {score}")

    # 计算老师所教学生的平均成绩
    print("\nTeacher Average Marks:")
    for teacher in school.teachers:
        print("- ", teacher.get_details())
        print(f"  Average Marks: {teacher.average_marks()}")

# 测试
test_system()