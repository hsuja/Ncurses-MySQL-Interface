# Alan Grubb
# Michael Siegel
# Jason Hsu
# CS419-400
# Final Project

import math
import MySQLdb
import curses
from curses import wrapper

def get_name(list, page, y_pos):

     for x in list:
	  if x[1] == page and x[2] == y_pos:
	       return x[0]

     return -1

def get_field(list, page, y_pos):

     for x in list:
	  if x[1] == page and x[2] == y_pos:
	       return x[0][0]

     return -1

def draw_list(list, cur_page, window):

     k = 1 + (cur_page - 1) * 10
     for y in list:
	  if y[1] == cur_page:
	       window.addstr(y[2], 0, str(k) + " " + y[0])
	       k += 1
     if cur_page > 1:
	  window.addstr(12, 0, "<- Prev Page")
     if cur_page < math.ceil(len(list) / 10.0):
	  window.addstr(13, 0, "-> Next Page")
     window.move(0, 0)

def draw_tableContent(list, cur_page, window, widths, num_columns):

     for y in list:
	  if y[1] == cur_page:
	       string = ""
	       i = 1
	       for k in y[0]:
		    if i > num_columns: break
		    string += str(k)
		    num_spaces = widths[i-1] - len(str(k))
		    if i != len(y[0]):
			 for j in range(num_spaces):
			      string += " "
		    i += 1

	       window.addstr(y[2], 0, string)
     if cur_page > 1:
	  window.addstr(10, 0, "<- Prev Page")
     if cur_page < math.ceil(len(list) / 10.0):
	  window.addstr(11, 0, "-> Next Page")
     window.move(0, 0)

def create_user(stdscr):
	#Allow user to see typed text
	curses.echo()

	#Create outer screen with title
	stdscr.clear()
	stdscr.border(0)
	stdscr.addstr(4, 34, "CREATE NEW USER", curses.A_STANDOUT)
	stdscr.refresh()

	#Create inner window for entry of database name
	begin_x = 22
	begin_y = 8
	height = 10
	width = 40
	win = curses.newwin(height, width, begin_y, begin_x)
	win.border(0)
	win.addstr(4, 12, "NAME: ")
	win.addstr(6, 8, "PASSWORD: ")
	win.move(4, 18)
	win.refresh()

	username = win.getstr()
	win.move(6, 18)
	win.refresh()
	password = win.getstr()
	stdscr.addstr(20, 2, "Are you sure you want to add " + username + "? (y/n)")
	curses.noecho()
	stdscr.refresh()
	res = win.getch()
	if res == ord('y'):
		#login to db as an admin user1
		hostname_db = "45.49.78.62"
		db = MySQLdb.connect(host=hostname_db, user="user1", passwd="password1")
		if db.cursor():
			cursor = db.cursor()
			#add user
			query = "CREATE USER \'" + str(username) + "\'@\'%\' IDENTIFIED BY \'" + str(password) + "\';"
			cursor.execute(query)
			#set permissions for new user
			query = "GRANT ALL PRIVILEGES ON * . * TO \'" + str(username) + "\'@\'%\';"
			cursor.execute(query)

	main(stdscr)
	return

def create_db(stdscr, db):
	#Allow user to see typed text
	curses.echo()

	#Create outer screen with title
	stdscr.clear()
	stdscr.border(0)
	stdscr.addstr(4, 34, "CREATE NEW DATABASE", curses.A_STANDOUT)
	stdscr.refresh()

	#Create inner window for entry of database name
	begin_x = 22
	begin_y = 8
	height = 10
	width = 40
	win = curses.newwin(height, width, begin_y, begin_x)
	win.border(0)
	win.addstr(4, 8, "NAME: ")
	win.move(4, 18)
	win.refresh()

	#Get user input for database name
	db_name = win.getstr()
	stdscr.addstr(20, 2, "Are you sure you want to add " + db_name + "? (y/n)")
	stdscr.refresh()
	curses.noecho()
	res = win.getch()
	if res == ord('y'):
		#Create new database
		cursor = db.cursor()
		cursor.execute('CREATE DATABASE ' + db_name + ';')

	#Navigate back to database overview
	db_overview(stdscr, db)
	return

def create_table(stdscr, db, db_name):
	#Allow user to see typed text
	curses.echo()

	#Create outer screen with title
	y_offset = 4
	x_offset = 16
	count = -1
	stdscr.clear()
	stdscr.border(0)
	stdscr.addstr(1, 34, "CREATE NEW TABLE", curses.A_STANDOUT)
	stdscr.addstr(22, 2, "A - Add Column    E - Execute    B - BACK        Q - QUIT")
	stdscr.addstr(y_offset, x_offset, "NAME: ")
	stdscr.refresh()
	stdscr.move(4, 22)
	table_name = stdscr.getstr()
	stdscr.move(19, 15)
	primary_key_used = False

	
	col_names = []
	data_types = []
	data_type_sizes = []
	options = []

	while 1:
		curses.noecho()
		input = stdscr.getch()

		if input == ord('a'):
			count += 1
			y_offset += 1
			curses.echo()
			stdscr.refresh()
			#store strings for column to be made
			stdscr.addstr(19, 14, "                                                                   ")
			stdscr.addstr(19, 2, "Column Name:")
			stdscr.refresh()
			stdscr.move(19, 15)
			col_names.append(stdscr.getstr())
			stdscr.addstr(19, 2, "  Data Type:")
			stdscr.addstr(19, 14, "                                                                   ")
			stdscr.refresh()
			stdscr.move(19, 15)
			data_types.append(stdscr.getstr())
			stdscr.addstr(19, 2, "  Data Size:")
			stdscr.addstr(19, 14, "                                                                   ")
			stdscr.refresh()
			stdscr.move(19, 15)
			data_type_sizes.append(stdscr.getstr())
			stdscr.addstr(19, 2, "Options (NULL/NOT NULL/AUTO_INCREMENT): ")
			stdscr.refresh()
			options.append(stdscr.getstr())
			stdscr.addstr(19, 2, "                                                                    ")
			#update view with added column
			stdscr.addstr(y_offset, x_offset, "COL" + str(count + 1) + ": " + col_names[count] + " " + data_types[count] + "(" + data_type_sizes[count] + ") " + options[count])
			stdscr.refresh()
			stdscr.move(19, 15)


		elif input == ord('e'):
			if len(col_names) == 0:
				stdscr.addstr(19, 2, "ERROR: Invalid query a table must contain at least one column.")
				stdscr.refresh()
			else:
				#build query	
				query = "CREATE TABLE " + table_name + "("
				for i in range(0, len(col_names)):
					query += str(col_names[i]) + " " + str(data_types[i])
					query += "(" + str(data_type_sizes[i]) + ")"
					if len(options[i]) > 0:
						query += " " + options[i]
					if len(col_names) > 1 and i != len(col_names) - 1:
						query += ","
				#if primary key not set, prompt user
				if primary_key_used == False:
					stdscr.addstr(19, 2, "Would you like to add a primary key to your table? (y/n)")
					stdscr.refresh()
					res = stdscr.getch()
					if res == ord('y'):
						stdscr.addstr(19, 2, "                                                            ")
						stdscr.refresh()
						curses.echo()
						stdscr.addstr(19, 2, "Enter the column number (1 - " + str(len(col_names)) + "):  ")
						stdscr.refresh()
						primary_key_index = stdscr.getstr()
						query += ", PRIMARY KEY (" + str(col_names[0]) + ")"
				query += ")ENGINE=INNODB;"
				#execute query
				cursor = db.cursor()
				cursor.execute(query)
				table_overview(stdscr, db, db_name)
				return

		elif input == ord('b'):
			table_overview(stdscr, db, db_name)
			return

		elif input == ord('q'): 
			curses.endwin()
			exit()
	
def db_overview(stdscr, db):

     curses.noecho() #do not display keyboard input
     curses.curs_set(1)

     cur_page = 1 
     page_num = 1

     cursor = db.cursor()
     cursor.execute("SHOW DATABASES")
     data = cursor.fetchall()

     stdscr.clear()
     stdscr.border(0)
     stdscr.addstr(4, 34, "DATABASES OVERVIEW", curses.A_STANDOUT)
     
     db_list = []
     i = 0
     for x in data:
	  #Append 3-tuple: (database, page number, y-pos of printed line)
	  db_list.append((x[0], page_num, i))
	  i += 1
	  if i == 10: 
	       page_num += 1
	       i = 0
    
     #10 listings per page
     num_pages = math.ceil(len(db_list) / 10.0)

     begin_x = 34
     begin_y = 6
     height = 15
     width = 40
     list_win = curses.newwin(height, width, begin_y, begin_x)
     list_win.keypad(1)
     
     #draw list
     draw_list(db_list, cur_page, list_win)
	  

     stdscr.addstr(22, 2, "U - USE    D - DROP    C - CREATE NEW DATABASE        Q - QUIT")
     stdscr.refresh()
     list_win.refresh()
     
     #handle key presses

     while 1:
	  input = list_win.getch()
	  cur_pos = list_win.getyx()
	  #stdscr.addstr(1,1, str(input))
	  if input == curses.KEY_UP:
	       if cur_pos[0] > 0:
		    list_win.move(cur_pos[0] - 1, cur_pos[1])
	  elif input == curses.KEY_DOWN: 
	       if cur_pos[0] < 9 and cur_pos[0] < (len(db_list) - (cur_page - 1) * 10) - 1:
		    list_win.move(cur_pos[0] + 1, cur_pos[1])
	       
	  elif input == curses.KEY_LEFT:
	       if cur_page > 1:
		    cur_page -= 1
		    list_win.erase()
		    draw_list(db_list, cur_page, list_win)


	  elif input == curses.KEY_RIGHT:
	       if cur_page < num_pages:
		    cur_page += 1
		    list_win.erase()
		    draw_list(db_list, cur_page, list_win)
	  elif input == ord('u'): 
	       db_name = get_name(db_list, cur_page, cur_pos[0])
	       table_overview(stdscr, db, db_name)
	       return
	  elif input == ord('d'): 
	       db_name = get_name(db_list, cur_page, cur_pos[0])
	       stdscr.addstr(21, 2, "Are you sure you want to DROP " + db_name + "? (y/n)")
	       res = stdscr.getch()
	       if res == ord('y'):
		    cursor.execute("DROP DATABASE  " + db_name)
		    db_overview(stdscr, db)
		    return
	       else:
		    db_overview(stdscr, db)
		    return
	  elif input == ord('c'):
	       create_db(stdscr, db)
	       return	
	  elif input == ord('q'): 
	       curses.endwin()
	       exit()

	  stdscr.refresh()
	  list_win.refresh()
    
     


def table_overview(stdscr, db, db_name):

     cur_page = 1
     page_num = 1

     cursor = db.cursor()
     sql = "USE " + db_name
     cursor.execute(sql)
     cursor.execute("SHOW TABLES")
     data = cursor.fetchall()

     stdscr.clear()
     stdscr.border(0)
     stdscr.addstr(4, 34, "TABLES IN " + db_name, curses.A_STANDOUT)

     table_list = []
     i = 0
     for x in data:
	  #Append 3-tuple: (table name, page, printed line)
	  table_list.append((x[0], page_num, i))
	  i += 1
	  if i == 10:
	       page_num += 1
	       i = 0
     
     
     #10 listings per page
     num_pages = math.ceil(len(table_list) / 10.0)

     begin_x = 34
     begin_y = 6
     height = 15
     width = 40
     list_win = curses.newwin(height, width, begin_y, begin_x)
     list_win.keypad(1)
     
     draw_list(table_list, cur_page, list_win)
      
     stdscr.addstr(22, 2, "V - VIEW    D - DELETE    C - CREATE TABLE    B - BACK        Q - QUIT")
     stdscr.refresh()
     list_win.refresh()
     
     #handle key presses

     while 1:
	  input = list_win.getch()
	  cur_pos = list_win.getyx()
	  
	  if input == curses.KEY_UP:
	       if cur_pos[0] > 0:
		    list_win.move(cur_pos[0] - 1, cur_pos[1])
	  elif input == curses.KEY_DOWN:
	       if cur_pos[0] < 9 and cur_pos[0] < (len(table_list) - (cur_page - 1) * 10) - 1:
		    list_win.move(cur_pos[0] + 1, cur_pos[1])
	  elif input == curses.KEY_LEFT:
	       if cur_page > 1:
		    cur_page -= 1
		    list_win.erase()
		    draw_list(table_list, cur_page, list_win)
	  elif input == curses.KEY_RIGHT:
	       if cur_page < num_pages:
		    cur_page += 1
		    list_win.erase()
		    draw_list(table_list, cur_page, list_win)
	       
	  elif input == ord('v'):
	       #view
	       table_name = get_name(table_list, cur_page, cur_pos[0])
	       table_contents(stdscr, db, db_name, table_name)
	       return
	  elif input == ord('d'): #delete table 
	       table_name = get_name(table_list, cur_page, cur_pos[0])
	       stdscr.addstr(21, 2, "Are you sure you want to DROP " + table_name + "? (y/n)")
	       res = stdscr.getch()
	       if res == ord('y'):
		    cursor.execute("DROP TABLE  " + table_name)
		    table_overview(stdscr, db, db_name)
		    return
	       else:
		    table_overview(stdscr, db, db_name)
		    return
	  elif input == ord('c'): 
	       create_table(stdscr, db, db_name)
	       return
	  elif input == ord('b'):
	       #back
	       db_overview(stdscr, db)
	       
	  elif input == ord('q'):
	       #quit
	       curses.endwin()
	       exit()

	  stdscr.refresh()
	  list_win.refresh()


def table_contents(stdscr, db, db_name, table_name):

     cur_page = 1
     page_num = 1

     curses.noecho()

     cursor = db.cursor()
     sql = "DESCRIBE " + table_name
     cursor.execute(sql)

     table_desc = cursor.fetchall()

     var_list = []
     type_list = []
     for x in table_desc:
	  var_list.append(x[0])
	  type_list.append(x[1])

     #Find lengths of var names
     #Initialize field_lengths and max_lengths
     var_lengths = []
     field_lengths = []
     max_widths = []
     for x in var_list:
	  var_lengths.append(len(x))
	  field_lengths.append(0)
	  max_widths.append(0)
     
     #Build query
     query = "SELECT "
     i = 1
     for var in var_list:
	  query += var
	  if i != len(var_list):
	       query += ","
	  query += " "
	  i += 1
     query += "FROM " + table_name
     
     cursor.execute(query)
     data = cursor.fetchall()

     stdscr.clear()
     stdscr.border(0)
     stdscr.addstr(4, 34, "CONTENTS IN " + table_name, curses.A_STANDOUT)

     #test print
     #stdscr.addstr(1,1, str(table_desc))
     #stdscr.addstr(2,1, str(var_list))
     #stdscr.addstr(2,1, str(data))
     #stdscr.addstr(2,1, str(var_lengths))

     contents_list = []
     i = 0
     for x in data:
	  fields_list = []
	  for y in x:
	       fields_list.append(y)
	  
	  #Find max length of fields
	  j = 0
	  for field in fields_list:
	       if len(str(field)) > field_lengths[j]:
		    field_lengths[j] = len(str(field))
	       j += 1
	  
	  #Append 3-tuple: ([list of fields], page, printed line)
	  contents_list.append((fields_list, page_num, i))
	  i += 1
	  if i == 10:
	       page_num += 1
	       i = 0
    

     for i in range(len(var_list)):
	  max_widths[i] = max(var_lengths[i], field_lengths[i]) + 1

     #10 listings per page
     num_pages = math.ceil(len(contents_list) / 10.0)

     begin_x = 2
     begin_y = 7
     height = 14
     width = 77
     list_win = curses.newwin(height, width, begin_y, begin_x)
     list_win.keypad(1)
     
     #Calculate number of columns
     total_width = 0
     num_columns = 0
     j = 1
     for i in max_widths:
	  total_width += i
	  if total_width >= (width - begin_x):
	       break
	  num_columns = j
	  j += 1

     #test print
     #stdscr.addstr(3,1, str(field_lengths))
     #stdscr.addstr(4,1, str(max_widths))
     #stdscr.addstr(5,1, "num_columns=" + str(num_columns))
     
     draw_tableContent(contents_list, cur_page, list_win, max_widths, num_columns)

     header = ""
     i = 1
     for x in var_list:
	  if i > num_columns: break
	  header += x
	  num_spaces = max_widths[i-1] - len(str(x))
	  if i != len(var_list):
	       for j in range(num_spaces):
		    header += " "
	  i += 1

     stdscr.addstr(6, 2, header, curses.A_UNDERLINE)
     stdscr.addstr(22, 2, "A - ADD ROW    E - EDIT    D - DELETE     B - BACK        Q - QUIT")
     stdscr.refresh()
     list_win.refresh()
	 
     while 1:
	  input = list_win.getch()
	  cur_pos = list_win.getyx()
	  
	  if input == curses.KEY_UP:
	      if cur_pos[0] > 0:
		   list_win.move(cur_pos[0] - 1, cur_pos[1])
	  elif input == curses.KEY_DOWN:
	      if cur_pos[0] < 9 and cur_pos[0] < (len(contents_list) - (cur_page - 1) * 10) - 1:
		   list_win.move(cur_pos[0] + 1, cur_pos[1])
	  elif input == curses.KEY_LEFT:
	      if cur_page > 1:
		   cur_page -= 1
		   list_win.erase()
		   draw_tableContent(contents_list, cur_page, list_win, max_widths, num_columns)
	  elif input == curses.KEY_RIGHT:
	      if cur_page < num_pages:
		   cur_page += 1
		   list_win.erase()
		   draw_tableContent(contents_list, cur_page, list_win, max_widths, num_columns)
	  elif input == ord('a'):
	       #Add row
	       curses.echo()
	       query = "INSERT INTO " + table_name + "("
	       stdscr.addstr(19, 2, "Add Row:")
	       new_fields = []
	       i = 1
	       for x in var_list:
		    query += x
		    if i != len(var_list):
			 query += ", "
		    stdscr.addstr(20, 2, type_list[i-1] + " " + x + "= ")
		    new_fields.append(stdscr.getstr())
		    stdscr.addstr(20, 2, "                                                                   ")
		    i += 1
		    #stdscr.addstr(1,1, str(new_fields))
	       query += ") VALUES ("
	       i = 1
	       for x in new_fields:
		    query += "'" + x + "'"
		    if i != len(new_fields):
			 query += ", "
		    i += 1
	       query += ")"
	       stdscr.addstr(2,1, "query= " + query)
	       cursor.execute(query)
	       db.commit()
	       table_contents(stdscr, db, db_name, table_name)
	       return
	  elif input == ord('e'):
	       #edit
	       curses.echo()
	       query = "UPDATE " + table_name + " SET "
	       stdscr.addstr(19, 2, "Update Row:")
	       new_fields = []
	       i = 1
	       for x in var_list:
		    query += x + "="
		    stdscr.addstr(20, 2, type_list[i-1] + " " + x + "= ")
		    query += "'" + stdscr.getstr() + "'"
		    if i != len(var_list):
			 query += ", "
		    stdscr.addstr(20, 2, "                                                                   ")
		    i += 1
		    #stdscr.addstr(1,1, str(new_fields))
	       
	       first_field = get_field(contents_list, cur_page, cur_pos[0])
	       
	       query += " WHERE " + var_list[0] + " = '" + str(first_field) + "'"
	       #stdscr.addstr(2,1, "query= " + query)
	       cursor.execute(query)
	       db.commit()
	       table_contents(stdscr, db, db_name, table_name)
	       return
	  elif input == ord('d'): #delete row 
	       first_field = get_field(contents_list, cur_page, cur_pos[0])
	       query = "DELETE FROM " + table_name + " WHERE " 
	       query += var_list[0] + " =  '" + str(first_field) + "'"
	       query += " LIMIT 1"
	       stdscr.addstr(21, 2, "Execute " + query + " (y/n)?")
	       res = stdscr.getch()
	       if res == ord('y'):
		    cursor.execute(query)
		    db.commit()
		    table_contents(stdscr, db, db_name, table_name)
		    return
	       else:
		    table_contents(stdscr, db, db_name, table_name)
		    return
	  elif input == ord('b'):
		   #back
		   table_overview(stdscr, db, db_name)

	  elif input == ord('q'):
	       #quit
	       curses.endwin()
	       exit()
			
	  stdscr.refresh()
	  list_win.refresh()
	  

def main(stdscr):
	stdscr = curses.initscr()
	stdscr.clear()
	curses.noecho()
	curses.curs_set(0)
	stdscr.border(0)

	stdscr.addstr(4, 22, "CS419 Group 1 Curses-Based MySQL Manager", curses.A_STANDOUT)
	stdscr.addstr(22, 2, "E - EXISTING USER    N - NEW USER")
	stdscr.addstr(12, 28, "EXISTING USER or NEW USER?")


	res = None
	while 1:
	     res = stdscr.getch()
	     if res == ord('e'):
		  stdscr.addstr(22, 2, "                                 ")
		  curses.echo()
		  curses.curs_set(1)
		  break
	     if res == ord('n'):
		  curses.curs_set(1)
		  create_user(stdscr)
		  return


	begin_x = 22
	begin_y = 8
	height = 10
	width = 40
	win = curses.newwin(height, width, begin_y, begin_x)

	win.border(0)
	
	win.addstr(0, 0, "ENTER LOGIN CREDENTIALS")
	win.addstr(3, 8, "Username: ")
	win.addstr(5, 8, "Password: ")
	win.move(3, 18)
	stdscr.refresh()
	win.refresh()

	username_db = win.getstr()
	win.move(5, 18)
	win.refresh()
	curses.noecho()
	password_db = win.getstr()
	curses.curs_set(0)
	hostname_db = "45.49.78.62"

	db = MySQLdb.connect(host=hostname_db, user=username_db, passwd=password_db)
	if db.cursor():
		stdscr.addstr(20, 30, "Connected!")
		db_overview(stdscr, db)

	#incorrect credentials produce ugly traceback. does not fail gracefully.
	else:
		stdscr.addstr(20, 30, "Connection failed.")
	
	#stdscr.addstr(21, 30, "", curses.A_BLINK)
	
	db.close()

	stdscr.getch()

	curses.endwin()

wrapper(main)