from fastapi import APIRouter,Depends,status
from fastapi import HTTPException
from database.connection import get_db_connection
from schemas.budget import BudgetCreate,BudgetUpdate,BudgetStatus
from routes.auth import get_current_user
#creating router for budget endpoints
router=APIRouter(prefix="/budgets",tags=["Budgets"])

#Reading all budgets
@router.get("/")
def get_budgets(current_user_id:int =Depends(get_current_user)):
    conn=get_db_connection()
    cur= conn.cursor()
    cur.execute(
        "SELECT * FROM budgets WHERE user_id=%s ORDER BY monthly_limit DESC ",
        (current_user_id,)
    )
    budgets=cur.fetchall()
    cur.close()
    conn.close()
    return budgets

#creating budgets
@router.post("/")
def add_budget(budget:BudgetCreate,current_user_id:int =Depends(get_current_user)):
    conn=get_db_connection()
    cur=conn.cursor()

    # Check if budget category already exists
    cur.execute("SELECT * FROM budgets WHERE category = %s AND user_id = %s", (budget.category,current_user_id))
    if cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Budget category already exists")


    cur.execute("INSERT INTO budgets(category,monthly_limit,user_id) VALUES(%s,%s,%s) RETURNING *",
         (budget.category,budget.monthly_limit,current_user_id)       
    )
    budget = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return budget

#updating budgets
@router.put("/{budgets_id}")
def update_budgets(budgets_id:int,budget:BudgetUpdate,current_user_id:int=Depends(get_current_user)):
    conn= get_db_connection()
    cur=conn.cursor()
   
    #only update fields that are provided
    update_data=budget.dict(exclude_unset=True)
   
    if not update_data:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No fields to update")


    #build dynamic sql query
    set_clause =",".join([f"{key}=%s" for key in update_data.keys()])
    values=list(update_data.values())
    values.extend([budgets_id,current_user_id])
   
   
   
   
   
    cur.execute(f"UPDATE budgets SET {set_clause} WHERE id= %s AND user_id = %s RETURNING *",
               values
    )
    updated=cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if updated:
        return updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")

#deleting budgets
@router.delete("/{budgets_id}")
def delete_budgets(budgets_id:int,current_user_id:int=Depends(get_current_user)):
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute("DELETE FROM budgets WHERE  id = %s  AND user_id = %s RETURNING *",(budgets_id,current_user_id))
    deleted=cur.fetchone()
    conn.commit()
    cur.close()
    if deleted:
        return{"message": "Budget deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Budget not found or you don't have permission to delete it "
    )


#getting the totals of budgets
@router.get("/total")
def get_totalbudgets(current_user_id:int=Depends(get_current_user)):
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute(
        "SELECT SUM(monthly_limit) as total FROM budgets WHERE user_id= %s",
    (current_user_id,)    
    )
    result=cur.fetchone()
    cur.close()
    conn.close()

    return{"total": result['total'] or 0}
#comparison between budget and the actual spend
@router.get("/status", response_model=list[BudgetStatus])
def get_budget_status(current_user_id: int = Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT
            b.category,
            b.monthly_limit,
            COALESCE(SUM(e.amount), 0) as spent,
            b.monthly_limit - COALESCE(SUM(e.amount), 0) AS remaining
        FROM budgets b
        LEFT JOIN expenses e
            ON b.category = e.category
            AND e.user_id = %s
            AND e.date >= date_trunc('month', CURRENT_DATE)
        WHERE b.user_id = %s
        GROUP BY b.category, b.monthly_limit                
    """, (current_user_id, current_user_id))
       # Passing current_user_id TWICE (once for expenses, once for budgets)
    
    results = cur.fetchall()
    cur.close()
    conn.close()

    # Adding over_budget flag
    status = []
    for row in results:
        status.append({
            "category": row['category'],
            "limit": row['monthly_limit'],
            "spent": row['spent'],
            "remaining": row['remaining'],
            "over_budget": row['remaining'] < 0
        })
    return status


