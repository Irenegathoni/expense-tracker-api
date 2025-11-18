from fastapi import APIRouter,Depends,status
from fastapi import HTTPException
from database.connection import get_db_connection
from schemas.expense import ExpenseCreate,ExpenseUpdate
from routes.auth import get_current_user  #import the auth dependancies
#creating a router for expense endpoints
router =APIRouter(prefix="/expenses",tags=["Expenses"])

#   creating expenses
@router.post("/")
def add_expense(expense:ExpenseCreate,current_user_id:int =Depends(get_current_user)):
    #creating a new expense for a logged in user,that is the expense will be linked to the current_user_id automatically
    
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute("INSERT INTO expenses(description,amount,category,date,user_id) VALUES(%s,%s,%s,%s,%s) RETURNING *",
            (expense.description,expense.amount,expense.category,expense.date,current_user_id)    
    )
    expense= cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return expense

#reading expenses
@router.get("/")
def get_expenses(current_user_id:int =Depends(get_current_user)):
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute(
        "SELECT * FROM expenses WHERE user_id =%s ORDER BY date DESC",
        (current_user_id,)
    )

    expenses=cur.fetchall()
    cur.close()
    conn.close()
    return expenses

#getting the totals of expenses
@router.get("/total")
def get_totalexpenses(current_user_id:int =Depends(get_current_user)):
    conn= get_db_connection()
    cur= conn.cursor()
    cur.execute(
        "SELECT SUM(amount) as total FROM expenses WHERE user_id=%s",
        (current_user_id,)
    )
    result=cur.fetchone()
    cur.close()
    conn.close()

    return{"total": result['total'] or 0}

#deleting expenses
@router.delete("/{expenses_id}")
def delete_expenses(expenses_id:int,current_user_id:int=Depends(get_current_user)):
    conn=get_db_connection()
    cur=conn.cursor()

    #deletes only if it belongs to the user
    cur.execute(
        "DELETE FROM expenses WHERE id = %s AND user_id=%s RETURNING *",
        (expenses_id,current_user_id)
        
    )
    deleted=cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted:
        return{"message": "Expense deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expense not found or you don't have permission to delete it"
    )

#updating expenses
@router.put("/{expenses_id}")
def update_expenses(expenses_id:int,expense:ExpenseUpdate,current_user_id:int=Depends(get_current_user)):
    conn=get_db_connection()
    cur=conn.cursor()
    
    #only update fields that are provided
    update_data=expense.dict(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    
    #build dynamic SQL query
    set_clause = "," .join([f"{key} =%s" for key in update_data.keys()])
    values=list(update_data.values())
    values.extend([expenses_id,current_user_id])


    cur.execute( f"UPDATE expenses SET {set_clause} WHERE id= %s AND user_id = %s RETURNING *",
         values
    )
   
    updated=cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated:
        return updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

#Daily expenses summary
@router.get("/summary/today")
def get_today_total(current_user_id:int=Depends(get_current_user)):
    conn=get_db_connection()
    cur= conn.cursor()
    cur.execute("""
        SELECT SUM(amount) as total
        FROM expenses
        WHERE date= CURRENT_DATE  AND user_id=%s     
    """,(current_user_id,))
    result=cur.fetchone()
    cur.close()
    conn.close()
    return{"period":"today", "total":result['total'] or 0}

#weekly expenses summary
@router.get("/summary/weekly")
def get_weekly_total(current_user_id:int=Depends(get_current_user)):
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute("""
        SELECT SUM(amount) as weekly_total
        FROM expenses
        WHERE date >= CURRENT_DATE - INTERVAL'7 days' 
        AND user_id= %s                     
    """, (current_user_id,))
    result=cur.fetchone()
    cur.close()
    conn.close()
    return{"period":"weekly", "weekly_total":result['weekly_total'] or 0}


#monthly summary expenses
@router.get("/summary/monthly")
def get_monthly_total(current_user_id:int=Depends(get_current_user)):
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute("""
        SELECT SUM(amount) AS monthly_total
        FROM  expenses
        WHERE date >=date_trunc('month',CURRENT_DATE)  
        AND user_id =%s                    
                               
    """,(current_user_id,))
    result=cur.fetchone()
    cur.close()
    conn.close()
    return{"period":"monthly","total":result['monthly_total'] or 0}


 