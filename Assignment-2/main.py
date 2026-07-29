from fastapi import FastAPI
from database import create_db , engine
from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate

app=FastAPI()
@app.on_event("startup")
def startup():
    create_db()
    with Session(engine) as session: 
        tasks= session.exec(select(Task)).all()
        if not tasks: 
            session.add(Task(title="Buy Books"))
            session.add(Task(title="Read Books"))
            session.add(Task(title="Buy another book"))
            session.commit()
@app.get("/tasks")
def get_tasks():
    with Session(engine) as session:
        return session.exec(select(Task)).all()

@app.get("/tasks/{task_id}")
def get_tasks(task_id:int):
    with Session(engine) as session:
        task= session.get(Task, task_id)
        if not task:
            return {"error":"Task not found"}
        return task

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(400, "Title Required")

    db_task= Task(title=task.title)
    with Session(engine) as session: 
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
    return db_task


@app.put("/tasks/{task_id}")
def update_task(task_id:int,updated:TaskUpdate):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(404,"Task not found in system")
        task.title=updated.title
        task.done=updated.done
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
@app.delete("/tasks/{task_id}")
def delete_task(task_id:int):
    with Session(engine) as session:
        task=session.get(Task,task_id)
        if not task: 
            raise HTTPException(404, "Task not found !")
            session.delete(task)
            session.commit()
        return {"Message":"task deleted"}
