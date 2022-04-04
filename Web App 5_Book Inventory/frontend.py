from tkinter import *
import backend

'''
A program that stores book information:
Title, Author
Year, ISBN (International Standard Book Number)

User can:

View all records
Search an entry
Add entry
Update entry
Delete
Close
'''

# Extracting info from the selected row
def get_selected_row(event):
    try: # if no IndexError, execute the lines below
        global selected_tuple
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[3])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[2])
        e4.delete(0, END)
        e4.insert(END, selected_tuple[4])
    except IndexError: # if IndexError occurs, pass ("do nothing" - listbox will remain empty)
        pass

# View All button
def view_command():
    list1.delete(0, END) # delete whatever was previously in the list book
    for row in backend.view():
        list1.insert(END, row) # new rows will be put at the end of the list box

# Search Entry button
def search_command():
    list1.delete(0, END) # delete whatever was previously in the list book
    # get values from what the user inserted in the text boxes, else assign an empty string
    for row in backend.search(title_text.get(), author_text.get(), year_text.get(), ISBN_text.get()):
        list1.insert(END, row)

# Add Entry button
def add_command():
    # get values from what the user inserted in the text boxes
    backend.insert(title_text.get(), author_text.get(), year_text.get(), ISBN_text.get())
    list1.delete(0, END)
    list1.insert(END, (title_text.get(), author_text.get(), year_text.get(), ISBN_text.get()))

# Delete button
def delete_command():
    backend.delete(selected_tuple[0])

# Update button
def update_command():
    # SET command is used with UPDATE to specify which columns and values that should be updated in a table
    backend.update(selected_tuple[0], title_text.get(), author_text.get(), year_text.get(), ISBN_text.get())

window = Tk() # creates an empty window

window.wm_title("BookStore") # Window Title

# Creating the GUI
# Adding Label Widgets to the window
l1 = Label(window, text = 'Title')
l1.grid(row = 0, column = 0)

l2 = Label(window, text = 'Year')
l2.grid(row = 1, column = 0)

l3 = Label(window, text = 'Author')
l3.grid(row = 0, column = 2)

l4 = Label(window, text = 'ISBN')
l4.grid(row = 1, column = 2)

# Adding Entry Widgets to the window
# StringVar - manage value of the widget
title_text = StringVar()
e1 = Entry(window, textvariable = title_text)
e1.grid(row = 0, column = 1)

year_text = StringVar()
e2 = Entry(window, textvariable = year_text)
e2.grid(row = 1, column = 1)

author_text = StringVar()
e3 = Entry(window, textvariable = author_text)
e3.grid(row = 0, column = 3)

ISBN_text = StringVar()
e4 = Entry(window, textvariable = ISBN_text)
e4.grid(row = 1, column = 3)

# Adding List Box Widget to the window
list1 = Listbox(window, height = 8, width = 50)
list1.grid(row = 2, column = 0, rowspan = 6, columnspan = 2)

# Adding Scroll Bar Widget to the window
sb1 = Scrollbar(window)
sb1.grid(row = 2, column = 2, rowspan = 6)

sb2 = Scrollbar(window, orient = "horizontal")
sb2.grid(row = 8, column = 0, columnspan = 3)

list1.configure(yscrollcommand = sb1.set) # vertical scroll bar along the y-axis will be set to this scroll bar & then go to the Scroll Bar method
sb1.configure(command = list1.yview) # when you scroll the bar, vertical view of the list will change

list1.configure(xscrollcommand = sb2.set) # vertical scroll bar along the y-axis will be set to this scroll bar & then go to the Scroll Bar method
sb2.configure(command = list1.xview) # when you scroll the bar, vertical view of the list will change

# Bind - used to bind a function to a widget event
# When row is selected, operate a specific operation on it
list1.bind('<<ListboxSelect>>', get_selected_row)

# Adding Button Widgets to the window
b1 = Button(window, text = 'View All', height = 1, width = 12, command = view_command)
b1.grid(row = 2, column = 3)

b2 = Button(window, text = 'Search Entry', height = 1, width = 12, command = search_command)
b2.grid(row = 3, column = 3)

b3 = Button(window, text = 'Add Entry', height = 1, width = 12, command = add_command)
b3.grid(row = 4, column = 3)

b4 = Button(window, text = 'Update', height = 1, width = 12, command = update_command)
b4.grid(row = 5, column = 3)

b5 = Button(window, text = 'Delete', height = 1, width = 12, command = delete_command)
b5.grid(row = 6, column = 3)

b6 = Button(window, text = 'Close', height = 1, width = 12, command = window.destroy)
b6.grid(row = 7, column = 3)

window.mainloop() # allows you to press the 'x' button in the corner of the window
