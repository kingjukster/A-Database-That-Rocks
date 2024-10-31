import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
def connectDB():
    return mysql.connector.connect(
                host="localhost",
                user="root",
                password="Superbowl2023",
                database="rockDB"
            )
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

def createUser():
    def submitUser():
        try:
            conn = connectDB()
            cursor = conn.cursor()
            
            userName = userNameEntry.get()
            cursor.execute("INSERT INTO users (userName) VALUES (%s)", (userName,))
            
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
    
    Label(addUserWindow, text="User Name:").grid(row=0, column=0, padx=10, pady=5)
    userNameEntry = Entry(addUserWindow)
    userNameEntry.grid(row=0, column=1, padx=10, pady=5)
    
    Button(addUserWindow, text="Create", command=submitUser).grid(row=6, columnspan=2, pady=10)
        

def loginUser():
    def checkUser():
        userName = userNameEntry.get()
        
        if not userName:
            messagebox.showerror("Error", "Username or password cannot be empty.")
            return
        
        try:
            conn = connectDB()
            cursor = conn.cursor()
            
            cursor.execute("""
                           SELECT * FROM users
                           WHERE userName=%s
                           """, (userName,))
            user = cursor.fetchone()
            #print(user)
            if user:
                global currentUserID
                currentUserID = user[0]
                titleFrame.pack_forget()
                messagebox.showinfo("Success", "User login successful!")
                loginWindow.destroy()
                showUserRockFrame(currentUserID)
            else:
                messagebox.showerror("Error", "Invalid username.")
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Failed to login.")
        finally:
            cursor.close()
            conn.close()

    loginWindow = Toplevel(root)
    loginWindow.title("Login")
    
    Label(loginWindow, text="User Name:").grid(row=0, column=0, padx=10, pady=5)
    userNameEntry = Entry(loginWindow)
    userNameEntry.grid(row=0, column=1, padx=10, pady=5)
    
    Button(loginWindow, text="Login", command=checkUser).grid(row=6, columnspan=2, pady=10)
        

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

def refreshRockTableData():
    for row in rockTable.get_children():
        rockTable.delete(row)
    populateRockTable()

def refreshUserRockTableData(userID=None):
    for row in userRockTable.get_children():
        userRockTable.delete(row)
    populateUserRockTable(userID)

#reveals rock table
def showRockFrame():
    userRockTableFrame.pack_forget()
    rockTableFrame.pack(fill=BOTH, expand=True)
    rockTableRefreshButton.pack(side=LEFT, padx=10)
    addRockButton.pack(side=LEFT, padx=10)
    switchToUserRockTable.pack(side=LEFT, padx=10)
    quitRockFrameButton.pack(side=RIGHT, padx=10)
    refreshRockTableData()

def showUserRockFrame(userID):
    rockTableFrame.pack_forget()
    userRockTableFrame.pack(fill=BOTH, expand=True)
    userRockTableRefreshButton.pack(side=LEFT, padx=10)
    addUserRockButton.pack(side=LEFT, padx=10)
    switchToRockTable.pack(side=LEFT, padx=10)
    quitUserRockFrameButton.pack(side=RIGHT, padx=10)
    refreshUserRockTableData(userID)

def retrieveImage(imageID):
    try:
        conn = connectDB()
        cursor = conn.cursor()
        
        cursor.execute("SELECT imageData FROM images WHERE imageID = %s", (imageID,))
        image = cursor.fetchone()
        
        if image:
            return image[0]
        else:
            print("Image not found.")
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def displayImage(imageID, frame, col, row):
    imageData = retrieveImage(imageID)
    
    if imageData:
        image = Image.open(io.BytesIO(imageData))
        image.thumbnail((100, 100))
        photo = ImageTK.PhotoImage(image)
        
        label = Label(frame, image=photo)
        label.image = photo
        label.pack(row=row, column=1, padx=10, pady=10)
    else:
        print("No image to display.")

root = Tk()
root.title("A Database that Rocks")

root.attributes("-fullscreen", True)
root.bind("<Escape>", toggleFullscreen)
root.bind("<Escape>", exitFullscreen)

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.geometry(f"{screenWidth}x{screenHeight}")


#this is the title frame
titleFrame = Frame(root)
titleFrame.pack(fill=BOTH, expand=True)

titleLabel = Label(titleFrame, text="A Database That Rocks", font=("Helvetica", 32))
titleLabel.pack(pady=100)

createUserButton = Button(titleFrame, text="Create User", font=("Helvetica", 20), command=createUser)
createUserButton.pack(pady=20)

loginButton = Button(titleFrame, text="Login", font=("Helvetica", 20), command=loginUser)
loginButton.pack(pady=20)

quitButton = Button(titleFrame, text="Quit", font=("Helvetica", 20), command=quitApp)
quitButton.place(relx=0.95, rely=0.95, anchor=SE)


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
switchToUserRockTable = Button(rockTableFrame, text="User Rocks", command=lambda: showUserRockFrame(currentUserID))
userRockTableRefreshButton = Button(userRockTableFrame, text="Refresh Data", command=lambda: refreshUserRockTableData(currentUserID))
addUserRockButton = Button(userRockTableFrame, text="Add Rock", command=addRock)
quitRockFrameButton = Button(rockTableFrame, text="Quit", command=quitApp)
quitUserRockFrameButton = Button(userRockTableFrame, text="Quit", command=quitApp)
switchToRockTable = Button(userRockTableFrame, text="View All Rocks", command=showRockFrame)


root.mainloop()