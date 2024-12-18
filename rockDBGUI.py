import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import hashlib
import io
import csv
#
def connectDB():
    return mysql.connector.connect(
                host="localhost",
                user="root",
                password="Superbowl2023",
                database="rockDB"
            )

#fill db with rocks (name, class, subclass) 11/7
def fillDB():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("""
           SELECT EXISTS (SELECT 1 FROM rocks);
           """)
    result = cursor.fetchone()  # This will return a tuple like (0,) or (1,)
    exists = result[0]
    if exists:
        return
    cursor.close()
    conn.close()

    csvPath = "rock.csv"
    with open(csvPath, encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            rockName = row[0]
            rockClass = row[1]
            rockSubClass = row[2]
            try:
                conn = connectDB()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO rocks (rockName, rockClass, rockSubClass) 
                    VALUES (%s, %s, %s)
                    """, (rockName, rockClass, rockSubClass))
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
    csvPath = "minerals.csv"
    with open(csvPath, encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            rockID = row[0]
            mineralID = row[1]
            try:
                conn = connectDB()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO minerals (mineralName, mineralHardness) 
                    VALUES (%s, %s)
                    """, (rockID, mineralID))
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
    csvPath = "rockmineral.csv"
    with open(csvPath, encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            rockID = row[0]
            mineralID = row[1]
            try:
                conn = connectDB()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO rockmineral (rockID, mineralID) 
                    VALUES (%s, %s)
                    """, (rockID, mineralID))
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
#this is the title frame
def titleScreen():
    global titleFrame
    titleFrame = Frame(root)
    root.config(bg='lightgrey')
    titleFrame.config(bg='darkgrey')
    titleFrame.grid(row=0, column=0, columnspan=3)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    titleLabel = Label(titleFrame, text="A Database That Rocks", font=("Helvetica", 32))
    titleLabel.grid(row=0, column=0, pady=(50, 20))
    titleLabel.config(bg='darkgrey')
    titleFrame.grid_rowconfigure(0, weight=1)
    titleFrame.grid_columnconfigure(0, weight=1)
    createUserButton = Button(titleFrame, text="Create User", font=("Helvetica", 20), command=createUser)
    createUserButton.grid(row=1, column=0, pady=(10, 10))
    createUserButton.config(bg='darkgrey')
    loginButton = Button(titleFrame, text="Login", font=("Helvetica", 20), command=loginUser)
    loginButton.grid(row=2, column=0, pady=(10, 10))
    loginButton.config(bg='darkgrey')
    quitButton = Button(titleFrame, text="Quit", font=("Helvetica", 20), command=quitApp)
    quitButton.grid(row=3, column=0, sticky="se", padx=20, pady=20)
    quitButton.config(bg='darkgrey')
#needs updated/removed
def populateRockTable():
    try:
        conn = connectDB()
        cursor = conn.cursor()
        cursor.execute("Select rockID, rockName, typeID, mineralComposition, locationFound, classification, rockDescription FROM rocks")
        rows = cursor.fetchall()
        
        for row in rows:
            rockTable.insert("", "end", values=row)
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
#needs updated/removed
def populateUserRockTable(userID=None):
    try:
        conn = connectDB()
        cursor = conn.cursor()
        if userID:
            cursor.execute("""
                SELECT r.rockID, r.rockName, r.typeID, r.mineralComposition, r.locationFound, r.classification, r.rockDescription, r.imageID
                FROM rocks r
                JOIN userRock ur ON r.rockID = ur.rockID
                WHERE ur.userID = %s
            """, (userID,))
#        else:
#            query = """
#                SELECT rockID, rockName, typeID, mineralComposition, locationFound, classification, rockDescription
#                FROM rocks
#            """
#            cursor.execute(query)
        
        rows = cursor.fetchall()

        for row in rows:
            print(rows)
            rockID, rockName, typeID, mineralComposition, locationFound, classification, rockDescription, imageID = row
        imageData = retrieveImage(imageID)
        photo = None
        if imageData:
            image = Image.open(io.BytesIO(imageData))
            image.thumbnail((100, 100))  # Resize image
            photo = ImageTk.PhotoImage(image)

        userRockTable.insert("", "end", values=row, image=photo)
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def toggleFullscreen(event=None):
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", exitFullscreen)

def exitFullscreen(event=None):
    root.attributes("-fullscreen", False)
    root.bind("<Escape>", toggleFullscreen)

def quitApp():
    root.quit()

#createUser updated 11/7
def createUser():
    def submitUser():
        try:
            conn = connectDB()
            cursor = conn.cursor()
            firstName = firstNameEntry.get()
            middleName = middleNameEntry.get() or None
            lastName = lastNameEntry.get()
            password = passwordEntry.get()
            salt = "RockyBestMovieEva"
            password += salt
            password = hashlib.md5(password.encode())
            cursor.execute("""
            INSERT INTO users (fName, mName, lName, userPassword)
            VALUES (%s, %s, %s, %s)
        """, (firstName, middleName, lastName, password.hexdigest()))
            conn.commit()
            messagebox.showinfo("Success", "User added successfully!")
            addUserWindow.destroy()
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Failed to add user.")
        finally:
            cursor.close()
            conn.close()

    addUserWindow = Toplevel(root)
    addUserWindow.title("Create User")
    
    Label(addUserWindow, text="First Name:").grid(row=0, column=0, padx=10, pady=5)
    firstNameEntry = Entry(addUserWindow)
    firstNameEntry.grid(row=0, column=1, padx=10, pady=5)
    ##
    Label(addUserWindow, text="Middle Name:").grid(row=1, column=0, padx=10, pady=5)
    middleNameEntry = Entry(addUserWindow)
    middleNameEntry.grid(row=1, column=1, padx=10, pady=5)
    ##
    Label(addUserWindow, text="Last Name:").grid(row=2, column=0, padx=10, pady=5)
    lastNameEntry = Entry(addUserWindow)
    lastNameEntry.grid(row=2, column=1, padx=10, pady=5)
    ##
    Label(addUserWindow, text="Password:").grid(row=3, column=0, padx=10, pady=5)
    passwordEntry = Entry(addUserWindow)
    passwordEntry.grid(row=3, column=1, padx=10, pady=5)
    ##
    Button(addUserWindow, text="Create", command=submitUser).grid(row=6, columnspan=2, pady=10)
        
#loginuser updated 11/7
def loginUser():
    def checkUser(event=None):
        global currentUserID
        userName = selected_user.get()
        password = passwordEntry.get()
        salt = "RockyBestMovieEva"
        password += salt
        password = hashlib.md5(password.encode())
        if not userName or not password.hexdigest():
            messagebox.showerror("Error", "Username or password cannot be empty.")
            return
        elif len(userName.split(" ")) == 2:
            fName, lName = userName.split(" ")
            #basic admin check
            if userName == "ADMIN ADMIN" and password.hexdigest() == "579d9814911e70768fa01ae064b1566f":
                #print("test")
                titleFrame.pack_forget()
                #root.withdraw()
                messagebox.showinfo("Success", "ADMIN login successful!")
                loginWindow.destroy()
                currentUserID = -1
                displayImage(currentUserID)#so you can still see posts as an admin
                return
            elif userName == "ADMIN ADMIN":
                messagebox.showerror("Error", "ADMIN password incorrect!")
                return
            #end of admin check
        else:
            fName, mName, lName = userName.split(" ")
        
        
        try:
            conn = connectDB()
            cursor = conn.cursor()
            if len(userName.split(" ")) == 3:
                cursor.execute("""
                            SELECT * FROM users
                            WHERE 
                            fName=%s 
                            AND mName=%s
                            AND lName=%s
                            AND userPassword=%s
                            """, (fName, mName, lName, password.hexdigest()))
                user = cursor.fetchone()
            else:
                cursor.execute("""
                            SELECT * FROM users
                            WHERE 
                            fName=%s 
                            AND lName=%s
                            AND userPassword=%s
                            """, (fName, lName, password.hexdigest()))
                user = cursor.fetchone()
            if user: 
                currentUserID = user[0]
                titleFrame.pack_forget()
                
                messagebox.showinfo("Success", "User login successful!")
                loginWindow.destroy()
                displayImage(currentUserID)
                #root.withdraw()
            else:
                messagebox.showerror("Error", "Invalid username.")
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Failed to login.")
        finally:
            cursor.close()
            conn.close()

    #global currentUserID
    loginWindow = Toplevel(root)
    loginWindow.title("Login")
    
    conn = connectDB()
    cursor = conn.cursor()        
    cursor.execute("""SELECT CONCAT_WS(' ', fName, mName, lName) as fullName FROM users""" )
    usernames = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    Label(loginWindow, text="User Name:").grid(row=0, column=0, padx=10, pady=5)
    selected_user = StringVar()
    selected_user.set(usernames[0])
    userNameDropdown = OptionMenu(loginWindow, selected_user, *usernames)
    userNameDropdown.grid(row=0, column=1, padx=10, pady=5)
    ##
    Label(loginWindow, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    passwordEntry = Entry(loginWindow)
    passwordEntry.focus_set()
    passwordEntry.grid(row=1, column=1, padx=10, pady=5)
    ##
    Button(loginWindow, text="Login", command=checkUser).grid(row=6, columnspan=2, pady=10)
    loginWindow.bind("<Return>", checkUser)
    

#created editUser 11/7
def editUser():
    def removeUser():
        userName = selected_user.get()
        if len(userName.split(" ")) == 3:
            firstName, middleName, lastName = userName.split(" ")
        else:
            firstName, lastName = userName.split(" ")
        try:
            conn = connectDB()
            cursor = conn.cursor()
            if len(userName.split(" ")) == 3:
                cursor.execute("DELETE FROM users WHERE fName = %s AND mName = %s AND lName = %s", (firstName, middleName, lastName))
            else:
                cursor.execute("DELETE FROM users WHERE fName = %s AND lName = %s", (firstName, lastName))
            conn.commit()
            messagebox.showinfo("Success", "User removed successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Failed to Remove.")
        finally:
            cursor.close()
            conn.close()
    
    def makeChanges():
        def saveEdits(userID):
            try:
                conn = connectDB()
                cursor = conn.cursor()
                firstName = firstNameEntry.get()
                middleName = middleNameEntry.get() or ""
                lastName = lastNameEntry.get() or ""
                password = passwordEntry.get()
                salt = "RockyBestMovieEva"
                password += salt
                password = hashlib.md5(password.encode())
                cursor.execute("""
                UPDATE users SET fName = %s, mName = %s, lName = %s, userPassword = %s
                WHERE userID = %s
            """, (firstName, middleName, lastName, password.hexdigest(), userID))
                conn.commit()
                messagebox.showinfo("Success", "User edited successfully!")
                editUserWindow.destroy()
                
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                messagebox.showerror("Error", "Failed to edit user.")
            finally:
                cursor.close()
                conn.close()
        
        try:
            userName = selected_user.get()
            firstName, middleName, lastName = userName.split(" ")
            conn = connectDB()
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT * FROM users
                        WHERE 
                        fName=%s 
                        AND mName=%s
                        AND lName=%s
                        """, (firstName, middleName, lastName))
            user = cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Failed to edit user.")
        finally:
            cursor.close()
            conn.close()
        editUserWindow = Toplevel(root)
        editUserWindow.title("Edit User")
        
        Label(editUserWindow, text="First Name:").grid(row=0, column=0, padx=10, pady=5)
        firstNameEntry = Entry(editUserWindow)
        firstNameEntry.insert(0, user[2])
        firstNameEntry.grid(row=0, column=1, padx=10, pady=5)
        ##
        Label(editUserWindow, text="Middle Name:").grid(row=1, column=0, padx=10, pady=5)
        middleNameEntry = Entry(editUserWindow)
        middleNameEntry.insert(0, user[3])
        middleNameEntry.grid(row=1, column=1, padx=10, pady=5)
        ##
        Label(editUserWindow, text="Last Name:").grid(row=2, column=0, padx=10, pady=5)
        lastNameEntry = Entry(editUserWindow)
        lastNameEntry.insert(0, user[4])
        lastNameEntry.grid(row=2, column=1, padx=10, pady=5)
        ##
        Label(editUserWindow, text="Password:").grid(row=3, column=0, padx=10, pady=5)
        passwordEntry = Entry(editUserWindow)
        passwordEntry.insert(0, user[1])
        passwordEntry.grid(row=3, column=1, padx=10, pady=5)
        ##
        Button(editUserWindow, text="Save", command=lambda: saveEdits(user[0])).grid(row=6, columnspan=2, pady=10)

    global currentUserID
    if currentUserID == -1:
        deleteWindow = Toplevel(root)
        deleteWindow.title("Delete Account")
        conn = connectDB()
        cursor = conn.cursor()        
        cursor.execute("""SELECT CONCAT_WS(' ', fName, mName, lName) as fullName FROM users""" )
        usernames = [row[0] for row in cursor.fetchall()]
        conn.close()
        Label(deleteWindow, text="User Name:").grid(row=0, column=0, padx=10, pady=5)
        selected_user = StringVar()
        selected_user.set(usernames[0])
        userNameDropdown = OptionMenu(deleteWindow, selected_user, *usernames)
        userNameDropdown.grid(row=0, column=1, padx=10, pady=5)
        Button(deleteWindow, text="Delete", command=removeUser).grid(row=6, columnspan=2, pady=10)
        Button(deleteWindow, text="Edit", command=makeChanges).grid(row=7, columnspan=2, pady=10)
    else:
        messagebox.showerror("Error", "ADMIN ONLY!")
            

#needs edited
def addRock():
    def submitRock():
        try:
            conn = connectDB()
            cursor = conn.cursor()
            
            rockName = rockNameEntry.get()
            typeID = typeIDEntry.get()
            mineralComposition = mineralCompositionEntry.get()
            locationFound = locationFoundEntry.get()
            classification = classificationEntry.get()
            rockDescription = rockDescriptionEntry.get()
            cursor.execute("""
                INSERT INTO rocks (rockName, typeID, mineralComposition, locationFound, classification, rockDescription)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (rockName, typeID, mineralComposition, locationFound, classification, rockDescription))
            
            conn.commit()
            messagebox.showinfo("Success", "Rock added successfully!")
            
            addRockWindow.destroy()
            
            refreshRockTableData()
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Failed to add rock.")
        finally:
            cursor.close()
            conn.close()
    
    addRockWindow = Toplevel(root)
    addRockWindow.title("Add New Rock")

    Label(addRockWindow, text="Rock Name:").grid(row=0, column=0, padx=10, pady=5)
    rockNameEntry = Entry(addRockWindow)
    rockNameEntry.grid(row=0, column=1, padx=10, pady=5)

    Label(addRockWindow, text="Type ID:").grid(row=1, column=0, padx=10, pady=5)
    typeIDEntry = Entry(addRockWindow)
    typeIDEntry.grid(row=1, column=1, padx=10, pady=5)

    Label(addRockWindow, text="Mineral Composition:").grid(row=2, column=0, padx=10, pady=5)
    mineralCompositionEntry = Entry(addRockWindow)
    mineralCompositionEntry.grid(row=2, column=1, padx=10, pady=5)

    Label(addRockWindow, text="Location Found:").grid(row=3, column=0, padx=10, pady=5)
    locationFoundEntry = Entry(addRockWindow)
    locationFoundEntry.grid(row=3, column=1, padx=10, pady=5)

    Label(addRockWindow, text="Classification:").grid(row=4, column=0, padx=10, pady=5)
    classificationEntry = Entry(addRockWindow)
    classificationEntry.grid(row=4, column=1, padx=10, pady=5)

    Label(addRockWindow, text="Rock Description:").grid(row=5, column=0, padx=10, pady=5)
    rockDescriptionEntry = Entry(addRockWindow)
    rockDescriptionEntry.grid(row=5, column=1, padx=10, pady=5)

    Button(addRockWindow, text="Submit", command=submitRock).grid(row=6, columnspan=2, pady=10)
#works somehow 11/12
def addPost():
    def submitPost():
        try:
            global currentUserID
            conn = connectDB()
            cursor = conn.cursor(buffered=True)
            
            rockName = selectedRock.get()
            cursor.execute("SELECT rockID FROM rocks WHERE rockName=%s", (rockName,))
            result = cursor.fetchone()
            if result:
                rockID = result[0]
            else:
                cursor.fetchall()
                messagebox.showerror("Error", "Rock not found in the database.")
                return
            rockColor = selectedColor.get()
            rockDescription = rockDescriptionEntry.get()
            image = imageEntry.get()
            #print(image)
            cursor.execute("""
                INSERT INTO posts (postDescription, postUserID, images, rockColor, rockID)
                VALUES (%s, %s, %s, %s, %s)
            """, (rockDescription, currentUserID, image, rockColor, rockID))
            conn.commit()
            messagebox.showinfo("Success", "Post added successfully!")
            
            addPostWindow.destroy()
            
            #need to edit
            #refreshRockTableData()
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Failed to add post.")
        finally:
            cursor.close()
            conn.close()
    def uploadImage():
        filePath = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("JPEG/PNG files", "*.jpg *.jpeg *.png")]
        )
        if filePath:
            imageEntry.delete(0, END)
            imageEntry.insert(0, filePath)

    addPostWindow = Toplevel(root)
    addPostWindow.title("Add New Post")
    addPostWindow.attributes("-topmost", True)

    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("SELECT rockName FROM rocks")
    rocks = [row[0] for row in cursor.fetchall()]
    Label(addPostWindow, text="Rock Name:").grid(row=0, column=0, padx=10, pady=5)
    selectedRock = StringVar(value=rocks[0])
    rockNameDropDown = OptionMenu(addPostWindow, selectedRock, *rocks)
    rockNameDropDown.grid(row=0, column=1, padx=10, pady=5)
    cursor.close()
    conn.close()

    colors = ['Black', 'Blue', 'Green', 'Orange', 'Purple', 'Red', 'White', 'Yellow']
    Label(addPostWindow, text="Rock Color:").grid(row=1, column=0, padx=10, pady=5)
    selectedColor = StringVar(value=colors[0])
    rockColorDropDown = OptionMenu(addPostWindow, selectedColor, *colors)
    rockColorDropDown.grid(row=1, column=1, padx=10, pady=5)

    Label(addPostWindow, text="Rock Description:").grid(row=2, column=0, padx=10, pady=5)
    rockDescriptionEntry = Entry(addPostWindow)
    rockDescriptionEntry.grid(row=2, column=1, padx=10, pady=5)
    
    Label(addPostWindow, text="Select Image:").grid(row=3, column=0, padx=10, pady=5)
    imageEntry = Entry(addPostWindow)
    imageEntry.grid(row=3, column=1, padx=10, pady=5)
    uploadButton = Button(addPostWindow, text="Upload", command=uploadImage)
    uploadButton.grid(row=3, column=2, padx=5, pady=5)

    Button(addPostWindow, text="Submit", command=submitPost).grid(row=4, columnspan=2, pady=10)
#needs updated/removed
def refreshRockTableData():
    for row in rockTable.get_children():
        rockTable.delete(row)
    populateRockTable()
#needs updated/removed
def refreshUserRockTableData(userID=None):
    for row in userRockTable.get_children():
        userRockTable.delete(row)
    populateUserRockTable(userID)

#reveals rock table
#needs updated/removed
def showRockFrame():
    userRockTableFrame.pack_forget()
    rockTableFrame.pack(fill=BOTH, expand=True)
    rockTableRefreshButton.pack(side=LEFT, padx=10)
    addRockButton.pack(side=LEFT, padx=10)
    addPostButton.pack(side = LEFT, padx = 10)
    switchToUserRockTable.pack(side=LEFT, padx=10)
    quitRockFrameButton.pack(side=RIGHT, padx=10)
    refreshRockTableData()
#needs updated/removed
def showUserRockFrame(userID):
    rockTableFrame.pack_forget()
    userRockTableFrame.pack(fill=BOTH, expand=True)
    userRockTableRefreshButton.pack(side=LEFT, padx=10)
    addUserRockButton.pack(side=LEFT, padx=10)
    switchToRockTable.pack(side=LEFT, padx=10)
    quitUserRockFrameButton.pack(side=RIGHT, padx=10)
    deleteUserUserRockFrameButton.pack(side=RIGHT, padx=10)
    refreshUserRockTableData(userID)

def LikePost(p):
    conn = connectDB()
    cursor = conn.cursor()
    #print(p[0],currentUserID)
    cursor.execute("SELECT userID FROM likes WHERE postID = %s AND userID = %s;", (p[0],currentUserID))
    likers = cursor.fetchall()
    skip = False
    if len(likers) == 0:
        cursor.execute("INSERT INTO likes (userID,postID) VALUES (%s , %s);",(currentUserID,p[0]))
        conn.commit()  # Commit the INSERT operation
        print(f"added a like, {p[0]}, {currentUserID}")
        return
    likers = likers[0]
    if currentUserID == likers[0]:
        cursor.execute("DELETE FROM likes WHERE postID = %s AND userID = %s;",(p[0],currentUserID))
        conn.commit()  # Commit the INSERT operation
        print("removed a like")
        
    updatelikes(p)
    cursor.close()
    conn.close()
    
    
def editPostfunc(p):
    def removePosts(p):
        try:
            conn = connectDB()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Likes WHERE postID =  %s ", (p[0],))
            conn.commit()
            cursor.execute("DELETE FROM posts WHERE postID = %s ", (p[0],))
            conn.commit()
            messagebox.showinfo("Success", "Post removed successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Failed to Remove.")
        finally:
            cursor.close()
            conn.close()
    
    def changePost(p):
        conn = connectDB()
        cursor = conn.cursor()
        try:
            des = desEntry.get()
            image = ImageEntry.get() 
            color = selectedColor.get() 
            rock = selectedRock.get()
            #print(rock)
            cursor.execute("SELECT rockID FROM rocks where rockName = %s",(rock,))
            #print(rock)
            rock = cursor.fetchone()  # This will return a tuple like (0,) or (1,)
            #print(rock)
            cursor.execute("""
            UPDATE posts SET postDescription = %s, images = %s, rockColor = %s, rockID = %s
            WHERE postID = %s
        """, (des,image,color,rock[0],p[0]))
            conn.commit()
            messagebox.showinfo("Success", "Post edited successfully!")
            editPostWindow.destroy()
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Failed to edit Post.")
        finally:
            cursor.close()
            conn.close()
        
    editPostWindow = Toplevel()
    editPostWindow.title(f"Post #{p[0]}")
    editPostWindow.geometry("400x700")
    conn = connectDB()
    cursor = conn.cursor()
    imagePath = p[3]
    if imagePath:
        try:
            image = Image.open(imagePath)
            image = image.resize((300, 300))
            photo = ImageTk.PhotoImage(image)
            imageLabel = Label(editPostWindow, image=photo)
            imageLabel.image = photo
            imageLabel.pack(pady=10)
        except Exception as e:
            Label(editPostWindow, text="Error loading image").pack()
            #print(f"Error loading image: {e}")
    #User Name
    cursor.execute("SELECT CONCAT_WS(' ', fName, mName, lName) as fullName FROM users WHERE userID=%s", (p[5],))
    user = cursor.fetchall()
    
    
    Label(editPostWindow, text="Image:").pack(pady=5)
    ImageEntry = Entry(editPostWindow)
    ImageEntry.insert(0, p[3])
    ImageEntry.pack(pady=5)
    Label(editPostWindow, text="Description:").pack(pady=5)
    desEntry = Entry(editPostWindow)
    desEntry.insert(0, p[1])
    desEntry.pack()
    #color
    colors = ['Black', 'Blue', 'Green', 'Orange', 'Purple', 'Red', 'White', 'Yellow']
    Label(editPostWindow, text="Rock Color:").pack(pady=5)
    selectedColor = StringVar(value=p[4])
    rockColorDropDown = OptionMenu(editPostWindow, selectedColor, *colors)
    rockColorDropDown.pack()
    #rock
    cursor.execute("SELECT rockName FROM rocks")
    rocks = [row[0] for row in cursor.fetchall()]
    Label(editPostWindow, text="Rock Name:").pack(pady=5)
    selectedRock = StringVar(value=rocks[p[5]])
    rockNameDropDown = OptionMenu(editPostWindow, selectedRock, *rocks)
    rockNameDropDown.pack()
    
    UpdatePost = Button(editPostWindow, text="Update Post", command=lambda: [changePost(p)])
    UpdatePost.pack()
    removepostButton = Button(editPostWindow, text="Remove Post", command=lambda: [removePosts(p)])
    removepostButton.pack()
    
    cursor.close()
    conn.close()

def updatelikes(p):
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS totalRows FROM likes WHERE postID = %s;", (p[0],))
    result = cursor.fetchone()
    numLikes = result[0]
    cursor.close()
    conn.close()
    return numLikes

#works right now it just displays all post with option for a detailed view
#takes in the currentUserID it doesn't use it right now but it could use it to display post a user made etc
def displayImage(currentUserID):
    def detailedView(p):
        detailedWindow = Toplevel()
        detailedWindow.title(f"Post #{p[0]}")
        detailedWindow.geometry("400x600")
        conn = connectDB()
        cursor = conn.cursor()
        imagePath = p[3]
        if imagePath:
            try:
                image = Image.open(imagePath)
                image = image.resize((300, 300))
                photo = ImageTk.PhotoImage(image)
                imageLabel = Label(detailedWindow, image=photo)
                imageLabel.image = photo
                imageLabel.pack(pady=10)
            except Exception as e:
                Label(detailedWindow, text="Error loading image").pack()
                #print(f"Error loading image: {e}")
        #User Name
        cursor.execute("SELECT CONCAT_WS(' ', fName, mName, lName) as fullName FROM users WHERE userID=%s", (p[5],))
        user = cursor.fetchall()
        if user == list:
            user = user[0]
            userName = user[0]
        else:
            userName = "Unknown User"
        userLabel = Label(detailedWindow, text=f"Posted by: {userName}", font=("Arial", 10))
        userLabel.pack(pady=5)
        #Rock Name
        cursor.execute("SELECT rockName FROM rocks WHERE rockID=%s", (p[5],))
        rocks = cursor.fetchall()
        rock = rocks[0]
        rockName = rock[0]
        rockLabel = Label(detailedWindow, text=f"Rock Name: {rockName}", font=("Arial", 10))
        rockLabel.pack(pady=5)
        #Rock Color
        colorLabel = Label(detailedWindow, text=f"Rock Color: {p[4]}", font=("Arial", 10))
        colorLabel.pack(pady=5)
        #Description
        descriptionLabel = Label(detailedWindow, text=f"Description: {p[1]}", font=("Arial", 10))
        descriptionLabel.pack(pady=5)
        #likes
        def refreshLikeLabel():
            likeCount = updatelikes(p)
            LikeLabel.config(text=f"Likes: {likeCount}")
        
        LikeLabel = Label(detailedWindow, text=f"Likes: {updatelikes(p)}", font=("Arial", 10))
        LikeLabel.pack(pady=5)
        likeButton = Button(detailedWindow, text="Like", command=lambda: [LikePost(p), refreshLikeLabel()])
        likeButton.pack()
        if currentUserID == -1 or currentUserID ==  p[2]:
            editPost = Button(detailedWindow, text="Edit Post", command=lambda: [editPostfunc(p), refreshLikeLabel()])
            editPost.pack()
        
        cursor.close()
        conn.close()
    def refresh(event=None, queryNum = 0):
        conn = connectDB()
        cursor = conn.cursor()
        filter, direction = selectedOption.get().split(" ")
        #direction = "DESC"
        filterQuery = f"SELECT * FROM posts ORDER BY {filter} {direction}"
        userPostQuery = f"SELECT * FROM posts WHERE postUserID={currentUserID} ORDER BY {filter} {direction}"
        queries = [filterQuery, userPostQuery]
        #print(queries[1])
        cursor.execute(queries[queryNum])
        posts = cursor.fetchall()
        #print(posts)
        #print(queryNum)
        for widget in root.winfo_children():
            if isinstance(widget, Frame) and widget != toolBarFrame:
                widget.destroy()
        for i, post in enumerate(posts):
            row = (i // columnsPerRow) + 1
            col = i % columnsPerRow
            cursor.execute("SELECT rockName FROM rocks WHERE rockID=%s", (post[5],))
            rocks = cursor.fetchall()
            rock = rocks[0]
            postFrame = Frame(root, borderwidth=1, relief="solid", padx=10, pady=10)
            postFrame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            postFrame.config(bg='darkgrey')
            titleLabel = Label(postFrame, text=f"{post[4]} {rock[0]}", font=("Arial", 12, "bold"), bg="darkgrey")
            titleLabel.pack()
            imagePath = post[3]
            if imagePath:
                try:
                    image = Image.open(imagePath)
                    image = image.resize((100, 100))
                    photo = ImageTk.PhotoImage(image)
                    imageLabel = Label(postFrame, image=photo)
                    imageLabel.image = photo
                    imageLabel.pack()
                except Exception as e:
                    Label(postFrame, text="Error loading image", bg="darkgrey").pack()
                    #print(f"Error loading image for post {i + 1}: {e}")
            viewButton = Button(postFrame, text="View", command=lambda p=post: {refresh,detailedView(p)})
            viewButton.pack()
        
        root.grid_rowconfigure(0, weight=0, minsize=50)
        for col in range(columnsPerRow):
            root.grid_columnconfigure(col, weight=1, uniform="posts")
    def removeFrames():
        for widget in root.winfo_children():
            if isinstance(widget, Frame):
                widget.destroy()

    #print(currentUserID)
    root.title("Posts")
    columnsPerRow = 3
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS totalRows FROM posts")
    result = cursor.fetchone()
    toolBarFrame = Frame(root, height=50)
    toolBarFrame.grid(row=0, column=0, sticky="n")
    toolBarFrame.config(bg='lightgrey')
    quitButton = Button(toolBarFrame, text="Quit", command=quitApp)
    quitButton.grid(row=0, column=0, padx=10, pady=10, sticky="ne")
    quitButton.config(bg='darkgrey')
    addPostButton = Button(toolBarFrame, text="Add Post", command=addPost)
    addPostButton.grid(row=0, column=1, padx=10, pady=10, sticky="ne")
    addPostButton.config(bg='darkgrey')
    options = ["postID ASC", "postID DESC", "rockColor ASC", "rockColor DESC", "postUserID ASC", "postUserID DESC", "rockID ASC", "rockID DESC"]
    selectedOption = StringVar()
    selectedOption.set(options[0])
    filterMenu = OptionMenu(toolBarFrame, selectedOption, *options, command=refresh)
    filterMenu.grid(row=0, column=2, padx=10, pady=10, sticky="ne")
    filterMenu.config(bg='darkgrey')
    def toggleAllPosts():
        userPostButton.grid_remove()
        allPostButton.grid(row=0, column=3, padx=10, pady=10, sticky="ne")
        refresh(None, 1)
    def toggleUserPosts():
        allPostButton.grid_remove()
        userPostButton.grid(row=0, column=3, padx=10, pady=10, sticky="ne")
        refresh()
    
    
    userPostButton = Button(toolBarFrame, text="View User Posts", command=toggleAllPosts)
    userPostButton.grid(row=0, column=3, padx=10, pady=10, sticky="ne")
    userPostButton.config(bg='darkgrey')
    allPostButton = Button(toolBarFrame, text="View All Posts", command=toggleUserPosts)
    allPostButton.config(bg='darkgrey')
    logoutButton = Button(toolBarFrame, text="Logout", command=lambda: [removeFrames(), titleScreen()])
    logoutButton.grid(row=0, column=4, padx=10, pady=10, sticky="ne")
    logoutButton.config(bg='darkgrey')
    if currentUserID == -1:
        deleteUser = Button(toolBarFrame, text="Edit Users", command=editUser)
        deleteUser.grid(row=0, column=5, padx=10, pady=10, sticky="ne")
        deleteUser.config(bg='darkgrey')
        
    toolBarFrame.grid_columnconfigure(0, weight=1)
    toolBarFrame.grid_columnconfigure(1, weight=1)
    toolBarFrame.grid_columnconfigure(2, weight=1)
    toolBarFrame.grid_columnconfigure(3, weight=1)
    toolBarFrame.grid_columnconfigure(4, weight=1)
    toolBarFrame.grid_columnconfigure(5, weight=1)
    refresh()
    cursor.close()
    conn.close()


currentUserID = -1
#titleFrame = None
fillDB() #this fills rock table with rocks 
root = Tk()
root.title("A Database that Rocks")

#root.attributes("-fullscreen", True)
root.bind("<Escape>", toggleFullscreen)
#root.bind("<Escape>", exitFullscreen)

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.geometry(f"{screenWidth}x{screenHeight}")
titleScreen()

"""
#this frame displays the rock table
rockTableFrame = Frame(root)
#rockTableFrame.pack(fill=BOTH, expand=TRUE) 
rockTable = ttk.Treeview(rockTableFrame, columns=("ID", "Name", "Type ID", "Mineral Composition", "Location Found", "Classification", "Rock Description"), show='headings')
rockTable.heading("ID", text="Rock ID")
rockTable.heading("Name", text="Name")
rockTable.heading("Type ID", text="Type ID")
rockTable.heading("Mineral Composition", text="Mineral Composition")
rockTable.heading("Location Found", text="Location Found")
rockTable.heading("Classification", text="Classification")
rockTable.heading("Rock Description", text="Rock Description")

rockTable.column("ID", width=100, anchor="center")
rockTable.column("Name", width=200, anchor="center")
rockTable.column("Type ID", width=100, anchor="center")
rockTable.column("Mineral Composition", width=200, anchor="center")
rockTable.column("Location Found", width=200, anchor="center")
rockTable.column("Classification", width=200, anchor="center")
rockTable.column("Rock Description", width=300, anchor="center")

rockTable.pack(fill=BOTH, expand=TRUE)
populateRockTable()



#this frame displays the userRock table
userRockTableFrame = Frame(root)
#userRockTableFrame.pack(fill=BOTH, expand=TRUE) 
userRockTable = ttk.Treeview(userRockTableFrame, columns=("Image", "ID", "Name", "Type ID", "Mineral Composition", "Location Found", "Classification", "Rock Description"), show='headings')
userRockTable.heading("Image", text="Image")
userRockTable.heading("ID", text="Rock ID")
userRockTable.heading("Name", text="Name")
userRockTable.heading("Type ID", text="Type ID")
userRockTable.heading("Mineral Composition", text="Mineral Composition")
userRockTable.heading("Location Found", text="Location Found")
userRockTable.heading("Classification", text="Classification")
userRockTable.heading("Rock Description", text="Rock Description")

userRockTable.column("Image", width=100, anchor="center")
userRockTable.column("ID", width=100, anchor="center")
userRockTable.column("Name", width=200, anchor="center")
userRockTable.column("Type ID", width=100, anchor="center")
userRockTable.column("Mineral Composition", width=200, anchor="center")
userRockTable.column("Location Found", width=200, anchor="center")
userRockTable.column("Classification", width=200, anchor="center")
userRockTable.column("Rock Description", width=300, anchor="center")

userRockTable.pack(fill=BOTH, expand=TRUE)
populateUserRockTable()

rockTableRefreshButton = Button(rockTableFrame, text="Refresh Data", command=refreshRockTableData)
addRockButton = Button(rockTableFrame, text="Add Rock", command=addRock)

#addPostButton = Button(root, text="Add Post", command=addPost)

switchToUserRockTable = Button(rockTableFrame, text="User Rocks", command=lambda: showUserRockFrame(currentUserID))

userRockTableRefreshButton = Button(userRockTableFrame, text="Refresh Data", command=lambda: refreshUserRockTableData(currentUserID))
addUserRockButton = Button(userRockTableFrame, text="Add Rock", command=addRock)
quitRockFrameButton = Button(rockTableFrame, text="Quit", command=quitApp)
quitUserRockFrameButton = Button(userRockTableFrame, text="Quit", command=quitApp)

deleteUserUserRockFrameButton = Button(userRockTableFrame, text="Edit Users", command=editUser)
switchToRockTable = Button(userRockTableFrame, text="View All Rocks", command=showRockFrame)
"""

root.mainloop()