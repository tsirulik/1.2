#Лабораторная работа №17.

##SQLAlchemy ORM
1) Спроектируйте БД с использованием crow’s foot notation.

2) Напишите модели данных, создайте и заполните БД с помощью SQLAlchemy.

3) Напишите запросы для выборки и анализа данных из БД.




Вариант 6:

Кафедры. Каждая кафедра имеет одного заведующего, который является преподавателем. Преподаватели могут работать на нескольких кафедрах одновременно.
Программы, решающая задачу

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date

Base = declarative_base()

class Department(Base):
    __tablename__= 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    head_id = Column(Integer, ForeignKey('teacher.id'))
    head = relationship("Teacher", back_populates="department", uselist=False)  # One-to-one
    teachers = relationship("Teacher", secondary="department_teacher", back_populates="departments")


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer, ForeignKey('department.id'))  # Исправлено: импорт ForeignKey
    department = relationship("Department", back_populates="head")
    departments = relationship("Department", secondary="department_teacher", back_populates="teachers")


class DepartmentTeacher(Base):
    __tablename__ = 'department_teacher'
    department_id = Column(Integer, ForeignKey('department.id'), primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id'), primary_key=True)


# создание базы данных
engine = create_engine('sqlite:///university.db')
Base.metadata.create_all(bind=engine)

# заполнение базы данных
session = sessionmaker(bind=engine)
session = session()

# добавление данных
department1 = Department(name='информатика', head_id=1)
department2 = Department(name='математика', head_id=2)

teacher1 = Teacher(name='иван иванов', department=department1)
teacher2 = Teacher(name='мария петрова', department=department2)
teacher3 = Teacher(name='алексей смирнов')
teacher3.departments.append(department1)
teacher3.departments.append(department2)

session.add(department1)
session.add(department2)
session.add(teacher1)
session.add(teacher2)
session.add(teacher3)
session.commit()

# получение всех кафедр
departments = session.query(Department).all()
print("кафедры:")
for dep in departments:
    print(f" - {dep.name}, заведующий: {dep.head.name}")

# получение всех преподавателей
teachers = session.query(Teacher).all()
print("\\nпреподаватели:")
for teach in teachers:
    print(f" - {teach.name}")

# получение преподавателей определенной кафедры
department_name = 'информатика'
department = session.query(Department).filter_by(name=department_name).first()
teachers_in_department = department.teachers
print(f"\\nпреподаватели кафедры '{department_name}':")
for teach in teachers_in_department:
    print(f" - {teach.name}")
```
