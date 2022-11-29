from typing import Optional, Union
import sqlite3

from fastapi import FastAPI
from pydantic import BaseModel


class Food(BaseModel):
    menu: str
    price: int


# create function for run SQL
def run_sql(
        sql_statement: str,
        value: Optional[tuple] = (),
        is_select: Optional[bool] = False
) -> Union[None, list]:

    # connect sqlite
    conn = sqlite3.connect("foods.db")
    cur = conn.cursor()
    cur.execute(sql_statement, value)

    # check select
    if is_select is True:
        list_of_foods = cur.fetchall()
        conn.commit()
        conn.close()
        return list_of_foods
    else:
        conn.commit()
        conn.close()


# Create database
run_sql(
    sql_statement="""
    CREATE TABLE IF NOT EXISTS foods
        (id INTEGER PRIMARY KEY,
        menu TEXT,
        price INTEGER)
    """
)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# get all foods
@app.get("/foods")
async def select_query():
    # Query
    result = run_sql(
        sql_statement="SELECT * FROM foods",
        is_select=True
    )
    return {"result": result}


# add new food
@app.post("/foods")
async def insert_food(food: Food):
    # Insert
    run_sql(
        sql_statement="INSERT INTO foods (menu, price) VALUES (?, ?)",
        value=(food.menu, food.price)
    )
    return {
        "name": food.menu,
        "desc": food.price,
    }


# edit food name form id
@app.patch("/foods/{id}")
async def update_food(id: int, food: Food):
    # update
    run_sql(
        sql_statement="UPDATE foods SET price = ? WHERE id = ?",
        value=(food.price, id)
    )
    return {
        "msg": f"edit food id:{id} completed"
    }


# delete food from id
@app.delete("/foods/{id}")
async def delete_food(id: int):
    run_sql(
        sql_statement="DELETE FROM foods WHERE id = ?",
        value=(id,)
    )
    return {
        "msg": f'delete food id:{id} completed',
    }


"""
Run FastAPI by use this command

>> python -m uvicorn foods:app --reload <<

main is name of file.py
app is name of FastAPI() <- line 47
"""
