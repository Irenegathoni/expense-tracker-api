#registration of a user

from fastapi import APIRouter,HTTPException,Depends,status # apirouter creates a group of related routes(all auth routes together). httpexception is used to return errors(email already exists).Depends checks if user is logged in. 
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials #Bearer sends a request to fastapi(tells fastapi) to expect a token in the authorization header. Authorizationcredentials-extracts the token from the request
import bcrypt #password hasher
import jwt #creates and verifies json web tokens
from datetime import datetime,timedelta # timedelta is used to set when tokens expire
import os # lets the environment variables to be read
from database.connection import get_db_connection #my function to connect to database
from schemas.user import UserRegister,UserLogin #import schemas



#creating a router for authentication routes
router=APIRouter(prefix="/auth",tags=["Authentication"]) #all functions with @router.post() or @router.ger belomg to this router
security=HTTPBearer() #sets up the security system

SECRET_KEY= os.getenv("SECRET_KEY","this-is-my-secret-key") #proves the token is real and was not tampered with
ALGORITHM="HS256" #HS256 = HMAC SHA-256 (a secure encryption algorithm)
ACCESS_TOKEN_EXPIRE_MINUTES=30

#settingup password hashing
def hash_password(password:str) -> str: #-> str means that the  function returns a string
    pwd_bytes=password.encode('utf-8') #converts the password string into bytes. utf-8 is the encoding format standard for text
    salt=bcrypt.gensalt() #salt is a random data added to the password before hashing and it makes each hash unique,even on the same password
    return bcrypt.hashpw(pwd_bytes,salt).decode('utf-8') #bcrypt.hashpw(pwd_bytes, salt) - Hashes the password with the salt..decode('utf-8') - Converts bytes back to a string..return - Returns the hashed password string


#verifying the password
def verify_password(plain_password:str,hashed_password:str) -> bool:
    #checking if a plain password matches the hashed version
    pwd_bytes=plain_password.encode('utf-8')
    hashed_bytes=hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes,hashed_bytes)


#creating access token function
def create_access_token(user_id: int) -> str:
    #creating a jwt token for a user
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
     
    payload={
        "user_id":user_id,
        "exp":expire
    } #payload is the data we put inside the token: the user and the when the token expires

    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM) #creates the actual jwt token
    return token
    
    #if the output of the token were to be "eyyyghatbfh7ujTY.evf2753Dbhye7Q.xyz123"
    #part1:header(algorithm info)
    #part2:payload(user_id,exp),it is encoded not encrypted ..meaning anyone can read the token
    #part3:signature(proves it is authentic)

#getting current user function
def get_current_user(credentials:HTTPAuthorizationCredentials = Depends(security)):
    #verifying jwt token and return the user_id
    token = credentials.credentials #credentials.credentials is the token string

    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id=payload.get("user_id") #extracting the user_id from the decoded payload

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return user_id
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.Please login again"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

        



#register function
@router.post("/register")
def register_user(user:UserRegister):
    conn=get_db_connection()
    cur=conn.cursor()
    #checking if the email already exists
    cur.execute("SELECT id FROM users WHERE email= %s",(user.email,))
    existing_user= cur.fetchone()

    if existing_user:
        cur.close()
        conn.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    #hashing the password
    hashed_password=hash_password(user.password)

    #inserting a new user
    cur.execute("INSERT INTO users(name,email,hashed_password) VALUES (%s,%s,%s) RETURNING id,name,email",
                (user.name,user.email,hashed_password)
    )
    new_user=cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    #returning the new user without password
    return{
        "message": "User registered successfully!",
        "user": new_user
    }

@router.post("/login")
def login_user(user:UserLogin):
    """
    login a user and return a JWT token
    Steps:
    1.Find user by email
    2.Verify password
    3.Create JWT token
    4.Return token

    the user must send this token with future requests to prove they are logged in

    """
    conn=get_db_connection()
    cur=conn.cursor()

    try:
        #step 1: find the user by email
        cur.execute(
            "SELECT id,name,email,hashed_password FROM users WHERE email= %s",
            (user.email,)
                    
        )
        db_user=cur.fetchone()

        #step2: verify password
        if not db_user or not verify_password(user.password,db_user['hashed_password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        #step3: create JWT token
        access_token=create_access_token(db_user['id'])

        #return token and user info
        return{
            "access_token":access_token,
            "token_type":"bearer",
            "user":{
                "id":db_user['id'],
                "name":db_user['name'],
                "email":db_user['email']
            }
        }
    finally:
        cur.close()
        conn.close()  


@router.get("/me")
def get_current_user_info(current_user_id:int =Depends(get_current_user)):
    """
    Get the logged-in user's information
    This is a protected route - a valid jwt token must be sent

    How to test:
    1.login to get a token
    2.click "authorize" button in swagger ui
    3.paste your token
    4.try this endpoint

    """
    conn=get_db_connection()
    cur=conn.cursor()

    cur.execute(
        "SELECT id,name,email  FROM users WHERE id=%s",
        (current_user_id,)
    )  
    user=cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )        
       
                               
    return user


