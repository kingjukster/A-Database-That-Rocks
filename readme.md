
Steps to run program

1. Run requirement.txt to get all dependencies.
2. run the entire SQL script in rockDB.sql to set up tables and data to be used for the GUI made.
3. Run the python file rockDBGUI.py this is the main GUI file and is used to fill other tables with information from the .csv files as well. 
4. Once in you can make an account with a password then login with the password. We have the signin as a drop down because there aren't going to be many users in test phase but it can be easily changed into a text field.
5. Once in you can make posts and add a picture to the post.


Run this to get all the correct programs needed to run the project.
pip install -r requirements.txt 

if it is giving squigglies for mysql.connector type this command into bash to fix it 
python -m pip install mysql-connector-python


# Completed
1. login()
2. createUser()
3. removeUser/editUser() *combined*
4. images **almost done**
5. addPost() **almost done** need to pull the frame to the front after uploading image
6. viewPosts()
7. logout()
8. likePost()

# In Progress
5. Move all buttons into the display function
# ToDo

1. modifyPost()
2. removePost()
3. queryInfo()
4. addMinerals()
5. addRock()


[rock dataset](https://en.wikipedia.org/wiki/List_of_rock_types)