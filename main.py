from fastapi import FastAPI 

app = FastAPI()

#storing expenses temporarily.
expenses=[] #list data structure

@app.post("/expenses")
def add_expense(description: str, amount: float, category: str,date:str):
    #dictionary data structure(hashmap)
    expense ={
        "id": len(expenses) + 1,
        "description": description,
        "amount":amount,
        "category": category,
        "date":date
    }
    expenses.append(expense) #adding  to a list
    return expense
    


@app.get("/expenses")
def get_expenses():
    return expenses

@app.get("/expenses/total")
def get_totalexpenses():
    total=0
    for exp in expenses:
       total += exp["amount"]  #getting a value from the dictionary
    return {"total":total}


@app.delete("/expenses/{expenses_id}")
def delete_expenses(expenses_id: int):
    for exp in expenses:
      if exp["id"]== expenses_id:
          expenses.remove(exp)
          return{"message":"Expense deleted successfully"}
    return{"error":"Expense not found"}
    
@app.put("/expenses/{expenses_id}")
def update_expenses(expenses_id:int,description:str, amount: float,category: str, date:str):
    for exp in expenses:
        if exp["id"] ==expenses_id:
           exp["description"] = description
           exp["amount"] = amount
           exp["category"] = category
           exp["date"] = date
        return(exp)  
    return{"error":"Expense not found"}
    