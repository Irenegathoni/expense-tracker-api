from fastapi import FastAPI
from routes import auth,expenses,budgets

#creating fastapi app
app=FastAPI(
    title="Expense Tracker",
    description="Tracking expenses and budgets ",
    version="1.0.0"
)  

#including all routers
app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(budgets.router)

#root endpoint
@app.get("/",tags=["Root"])
def root():
    return{
        "message":"Welcome to Expense Tracker",
        "status":"running",
        "docs":"Docs for API documentation"

    }
