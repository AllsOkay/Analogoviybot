from model.models import Base, Mark, Homework
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_mark(date, pupil_name, subject, mark):
    mark = Mark(date=date, pupil_name=pupil_name, subject=subject, mark=mark)
    session.add(mark)
    session.commit()

def get_marks(pupil_name):
    query = session.query(Mark.id, Mark.pupil_name, Mark.subject, Mark.date, Mark.mark).filter_by(pupil_name=pupil_name)
    return query

def delete_mark(id):
    try:
        mark = session.query(Mark).filter(Mark.id==id).first()
        session.delete(mark)
        session.commit()
        return True
    except:
        return False

def add_homework(date, subject, homework):
    user = Homework(date=date, subject=subject, homework_text=homework)
    session.add(user)
    session.commit()    

def get_homework(subject):
    query = session.query(Homework.id, Homework.subject, Homework.date, Homework.homework_text).filter_by(subject=subject)
    return query

def delete_homework(id):
    try:
        delete_homework = session.query(Homework).filter(Homework.id==id).first()
        session.delete(delete_homework)
        session.commit()
        return True
    except:
        return False
        
# Test reading marks
marks = get_marks('Иван Петров')
for row in marks:
    values = list(row._asdict().values())
    print(values)

# Test reading homeworks
homeworks = get_homework('Математика')
for row in homeworks:
    values = list(row._asdict().values())
    print(values)