import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

def connect_db():
    conn=sqlite3.connect("mydb.db")
    return conn

def create_table():
    conn=connect_db()
    cur=conn.cursor()
    cur.execute('create table if not exists student(name text,password text,roll_no int primary key,branch text)')
    conn.commit()
    conn.close()

def addrecord(data):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM student WHERE roll_no = ?', (data[2],))
    if cur.fetchone():
        st.error("User with this roll number already exists")
    else:
        cur.execute('insert into student(name, password, roll_no, branch) values(?,?,?,?)', data)
        conn.commit()
        st.success("Record added successfully")
    conn.close()
    
  
    
def view_record():
    conn=connect_db()
    cur=conn.cursor()
    cur.execute('select * from student')
    result=cur.fetchall()
    conn.close()
    return result

def disp():
    data=view_record()
    st.table(data)

def reset_password():
    st.title("Reset Password")
    roll_no = st.text_input('Enter your roll_no.')
    new_password = st.text_input('Enter new password', type='password')
    re_new_password = st.text_input('Re-enter new password', type='password')
    if st.button("Reset Password"):
        if new_password != re_new_password:
            st.error("Passwords do not match")
        else:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute('UPDATE student SET password = ? WHERE roll_no = ?', (new_password, roll_no))
            conn.commit()
            conn.close()
            st.success("Password reset successfully") 

def delete_user():
    st.title("Delete User")
    roll_no = st.text_input('Enter roll_no of the user to delete')
    if st.button("Delete User"):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM student WHERE roll_no = ?', (roll_no,))
        conn.commit()
        conn.close()
        st.success("User deleted successfully")  
        
def search_user():
    st.title("Search User")
    roll_no = st.text_input('Enter roll_no to search')
    if st.button("Search"):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM student WHERE roll_no = ?', (roll_no,))
        result = cur.fetchone()
        conn.close()
        if result:
            st.write(f"Name: {result[0]}, Roll No: {result[2]}, Branch: {result[3]}")
        else:
            st.error("User not found")
def sign_up():
    st.title("sign up")
    roll_no=st.text_input('enter your roll_no.')
    name=st.text_input('enter your name')
    branch=st.selectbox("branch",options=['cse','aiml','ece','me'])
    password=st.text_input('password',type='password')
    re_pass=st.text_input('re-try',type='password')
    if st.button("signin"):
        if password != re_pass:
            st.error("pass not matched")
        else:
            addrecord((name,password,roll_no,branch))
create_table()
with st.sidebar:
    select = option_menu('select from here', ['sign_up', 'display all record', 'reset password', 'delete user', 'search user'])

if select == 'sign_up':
    sign_up()
elif select == 'display all record':
    disp()
elif select == 'reset password':
    reset_password()
elif select == 'delete user':
    delete_user()
elif select == 'search user':
    search_user()
else:
    pass
    
