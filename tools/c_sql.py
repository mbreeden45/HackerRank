# SQL Foundations: sample tables, 4 reading lessons with runnable queries, and 32 practice problems.
# `expected` rows are produced here by running the reference solution with Python's sqlite3.
# `expect_count` is the number of rows worked out by hand, so a wrong solution cannot slip through unnoticed.
import sqlite3

TABLES = {
 "employees": dict(
  columns=[["id", "whole number", "unique number for each employee"], ["name", "text", "first name"], ["department", "text", "Sales, Engineering, HR or Support"], ["salary", "whole number", "yearly pay"], ["manager_id", "whole number or NULL", "the id of this person's manager, or NULL if they have none"], ["hire_year", "whole number", "year they joined"]],
  create="""CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER, manager_id INTEGER, hire_year INTEGER);
INSERT INTO employees VALUES (1,'Ava','Sales',52000,NULL,2015),(2,'Ben','Sales',48000,1,2018),(3,'Cara','Sales',45000,1,2020),
(4,'Dev','Engineering',90000,NULL,2014),(5,'Elle','Engineering',82000,4,2017),(6,'Finn','Engineering',76000,4,2019),(7,'Gia','Engineering',71000,4,2021),
(8,'Hugo','HR',50000,NULL,2016),(9,'Ivy','HR',47000,8,2022),(10,'Jon','Support',41000,NULL,2018),(11,'Kay','Support',39000,10,2020),(12,'Liam','Support',39000,10,2023);"""),
 "customers": dict(
  columns=[["id", "whole number", "unique number for each customer"], ["name", "text", "first name"], ["city", "text", "home city"], ["joined_year", "whole number", "year they became a customer"]],
  create="""CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT, joined_year INTEGER);
INSERT INTO customers VALUES (1,'Alice','Austin',2019),(2,'Bruno','Boston',2020),(3,'Chen','Austin',2021),(4,'Dana','Denver',2019),
(5,'Eli','Boston',2022),(6,'Fay','Chicago',2021),(7,'Gus','Denver',2023),(8,'Hana','Austin',2023);"""),
 "orders": dict(
  columns=[["id", "whole number", "unique number for each order"], ["customer_id", "whole number", "the id of the customer who ordered (see customers)"], ["product", "text", "what was bought"], ["amount", "whole number", "price in dollars"], ["order_date", "text", "date as YYYY-MM-DD"], ["status", "text", "shipped, pending or returned"]],
  create="""CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, product TEXT, amount INTEGER, order_date TEXT, status TEXT);
INSERT INTO orders VALUES (1,1,'Laptop',1200,'2023-01-15','shipped'),(2,1,'Mouse',25,'2023-02-10','shipped'),(3,2,'Desk',300,'2023-02-20','shipped'),
(4,3,'Chair',150,'2023-03-05','returned'),(5,2,'Monitor',220,'2023-03-18','shipped'),(6,4,'Laptop',1100,'2023-04-02','shipped'),
(7,5,'Mouse',25,'2023-04-11','pending'),(8,1,'Keyboard',60,'2023-05-07','shipped'),(9,3,'Monitor',230,'2023-05-21','shipped'),
(10,6,'Desk',310,'2023-06-01','pending'),(11,2,'Mouse',25,'2023-06-14','shipped'),(12,4,'Chair',140,'2023-07-09','shipped'),
(13,6,'Laptop',1250,'2023-07-30','shipped'),(14,5,'Keyboard',55,'2023-08-15','returned');"""),
 "accounts": dict(
  columns=[["id", "whole number", "unique number for each account"], ["customer_id", "whole number", "the id of the customer who owns it (see customers)"], ["type", "text", "checking or savings"], ["balance", "whole number", "money in the account, in dollars"], ["opened_year", "whole number", "year the account was opened"]],
  create="""CREATE TABLE accounts (id INTEGER PRIMARY KEY, customer_id INTEGER, type TEXT, balance INTEGER, opened_year INTEGER);
INSERT INTO accounts VALUES (1,1,'checking',2500,2019),(2,1,'savings',8000,2020),(3,2,'checking',150,2020),(4,3,'checking',4200,2021),
(5,4,'savings',12000,2019),(6,4,'checking',900,2022),(7,5,'savings',300,2022),(8,6,'checking',0,2021);"""),
}

STUDY = [
 dict(id="sql_select", track="SQL Foundations", title="SELECT and WHERE: asking a table for rows",
  blocks=[
   dict(t="p", text="SQL (said as sequel or S-Q-L) is the language for asking questions of a database. A database stores information in tables. A table is a grid: each row is one thing (one employee, one order) and each column is one fact about it (a name, a salary)."),
   dict(t="p", text="You do not tell SQL how to find the answer. You describe the answer you want, and the database works out the rest. That makes SQL short, but the words must be in the right order."),
   dict(t="h", text="The tables used in this app"),
   dict(t="p", text="Every practice problem uses the same four small tables: `employees`, `customers`, `orders` and `accounts`. Here are the first rows of `employees`. You can see every table with its columns on each practice screen."),
   dict(t="table", head=["id", "name", "department", "salary", "manager_id", "hire_year"], rows=[[1, "Ava", "Sales", 52000, "NULL", 2015], [2, "Ben", "Sales", 48000, 1, 2018], [4, "Dev", "Engineering", 90000, "NULL", 2014]], title="employees (first three of twelve rows)"),
   dict(t="h", text="SELECT ... FROM: choose columns"),
   dict(t="p", text="`SELECT` says which columns you want. `FROM` says which table. The star `*` means all columns. Press Run to try it. You can edit any query on this page and run it again."),
   dict(t="sql", label="All columns, all rows", text="SELECT * FROM employees;"),
   dict(t="sql", label="Only two columns", text="SELECT name, salary FROM employees;"),
   dict(t="callout", text="Keywords such as SELECT and FROM are usually written in capitals so they stand out. SQL does not mind either way. A semicolon at the end finishes the query."),
   dict(t="h", text="WHERE: choose rows"),
   dict(t="p", text="`WHERE` keeps only the rows where a condition is true. Compare with `=` (equal), `<>` (not equal), `<`, `>`, `<=` and `>=`. In SQL a single `=` does the comparing. Text goes in single quotes: `'Sales'`. Numbers do not."),
   dict(t="sql", label="Rows that match one condition", text="SELECT name, salary FROM employees WHERE department = 'Sales';"),
   dict(t="sql", label="Numbers need no quotes", text="SELECT name FROM employees WHERE salary > 70000;"),
   dict(t="h", text="Combining conditions"),
   dict(t="p", text="`AND` needs both conditions to be true. `OR` needs at least one. `NOT` flips a condition. Use brackets when you mix AND and OR, because AND is worked out first."),
   dict(t="sql", label="AND", text="SELECT name, salary FROM employees WHERE department = 'Engineering' AND salary < 80000;"),
   dict(t="h", text="More ways to filter"),
   dict(t="table", head=["Tool", "Meaning", "Example"], rows=[
     ["IN (a, b)", "equals one of several values", "product IN ('Mouse', 'Keyboard')"],
     ["BETWEEN a AND b", "from a to b, both ends included", "amount BETWEEN 100 AND 300"],
     ["LIKE", "text pattern: % means any run of characters", "name LIKE '%a' means ends with a"],
     ["IS NULL", "the value is missing (NULL means no value)", "manager_id IS NULL"],
     ["DISTINCT", "remove repeated rows from the result", "SELECT DISTINCT city FROM customers"]]),
   dict(t="warn", text="NULL is not zero and not an empty text. It means unknown or missing. You cannot test it with `= NULL`. Always write `IS NULL` or `IS NOT NULL`."),
   dict(t="sql", label="A missing value", text="SELECT name FROM employees WHERE manager_id IS NULL;"),
   dict(t="sql", label="Remove repeats", text="SELECT DISTINCT city FROM customers;"),
  ],
  after=dict(text="Practise SELECT and WHERE with real queries.", href="#/sql", button="Open the SQL practice list")),

 dict(id="sql_order", track="SQL Foundations", title="ORDER BY and LIMIT: sorting and trimming",
  blocks=[
   dict(t="p", text="A query result has no guaranteed order unless you ask for one. `ORDER BY` sorts the rows. `LIMIT` keeps only the first few rows. Together they answer questions such as who are the top three earners."),
   dict(t="sql", label="Smallest salary first (ASC is the default)", text="SELECT name, salary FROM employees ORDER BY salary;"),
   dict(t="sql", label="Biggest salary first: DESC means descending", text="SELECT name, salary FROM employees ORDER BY salary DESC;"),
   dict(t="h", text="Sorting by more than one column"),
   dict(t="p", text="Separate the columns with commas. SQL sorts by the first column, and only uses the second to break ties, and so on. Each column can have its own ASC or DESC."),
   dict(t="sql", label="Department A to Z, and inside each department the highest salary first", text="SELECT department, name, salary FROM employees ORDER BY department, salary DESC;"),
   dict(t="h", text="LIMIT: keep only the first rows"),
   dict(t="p", text="`LIMIT 3` keeps the first three rows of the sorted result. Always put it last in the query. Without ORDER BY, LIMIT gives an arbitrary three rows, so use them together."),
   dict(t="sql", label="The three highest paid", text="SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3;"),
   dict(t="h", text="Calculated columns and AS"),
   dict(t="p", text="You can calculate a new column with plain arithmetic, and give it a name with `AS`."),
   dict(t="sql", label="Yearly pay for a 5 percent raise", text="SELECT name, salary * 105 / 100 AS new_salary FROM employees ORDER BY new_salary DESC LIMIT 5;"),
   dict(t="callout", text="Order of the words matters: SELECT, FROM, WHERE, ORDER BY, LIMIT. Mixing them up is the most common beginner error."),
   dict(t="p", text="Dates stored as text in the form YYYY-MM-DD sort correctly in plain alphabetical order, so `ORDER BY order_date DESC` puts the newest order first."),
   dict(t="sql", label="The three newest orders", text="SELECT id, order_date FROM orders ORDER BY order_date DESC LIMIT 3;"),
  ],
  after=dict(text="Practise sorting and limiting.", href="#/sql", button="Open the SQL practice list")),

 dict(id="sql_join", track="SQL Foundations", title="JOIN: combining two tables",
  blocks=[
   dict(t="p", text="Databases split information into several tables so that nothing is stored twice. An order does not repeat the customer's name. It stores `customer_id`, a number that matches one row in the customers table. A column like that is called a key."),
   dict(t="table", head=["orders.id", "orders.customer_id", "orders.product"], rows=[[1, 1, "Laptop"], [3, 2, "Desk"]], title="orders (some rows)"),
   dict(t="table", head=["customers.id", "customers.name"], rows=[[1, "Alice"], [2, "Bruno"]], title="customers (some rows)"),
   dict(t="p", text="Order 1 has customer_id 1, and customer 1 is Alice. A `JOIN` lines the rows up like that and gives you one wide row with facts from both tables."),
   dict(t="h", text="INNER JOIN ... ON"),
   dict(t="p", text="`ON` says which columns must match. When two tables have a column with the same name, write the table name first and a dot: `orders.id`. Short nicknames called aliases save typing: `FROM orders o` lets you write `o.id`."),
   dict(t="sql", label="Each order with the customer's name", text="SELECT c.name, o.product, o.amount\nFROM orders o\nJOIN customers c ON o.customer_id = c.id;"),
   dict(t="p", text="A plain JOIN is an inner join: it keeps only rows that have a match on both sides. A customer with no orders disappears from the result."),
   dict(t="h", text="LEFT JOIN: keep everything from the left table"),
   dict(t="p", text="`LEFT JOIN` keeps every row from the table before the word JOIN, even when nothing matches. The columns from the other table are NULL for those rows. That lets you find things that have no match at all."),
   dict(t="sql", label="Customers who have never ordered", text="SELECT c.name\nFROM customers c\nLEFT JOIN orders o ON o.customer_id = c.id\nWHERE o.id IS NULL;"),
   dict(t="h", text="Watch out for repeated rows"),
   dict(t="p", text="If one customer has three orders, a join gives that customer three rows. To list each customer once, add DISTINCT, or group the rows (next lesson)."),
   dict(t="sql", label="Customers with at least one returned order, each listed once", text="SELECT DISTINCT c.name\nFROM customers c\nJOIN orders o ON o.customer_id = c.id\nWHERE o.status = 'returned';"),
   dict(t="h", text="Joining a table to itself"),
   dict(t="p", text="In `employees`, manager_id holds the id of another row in the same table. To show each employee next to their manager's name, join the table to itself and give each copy its own alias."),
   dict(t="sql", label="Employee and manager", text="SELECT e.name AS employee, m.name AS manager\nFROM employees e\nJOIN employees m ON e.manager_id = m.id;"),
  ],
  after=dict(text="Practise joins.", href="#/sql", button="Open the SQL practice list")),

 dict(id="sql_group", track="SQL Foundations", title="GROUP BY and HAVING: totals per group",
  blocks=[
   dict(t="p", text="So far each result row came from one table row. To answer questions such as how many employees are in each department, you collapse many rows into one per group. Functions that collapse rows are called aggregates."),
   dict(t="table", head=["Function", "What it gives"], rows=[["COUNT(*)", "how many rows"], ["SUM(col)", "the total of a column"], ["AVG(col)", "the average"], ["MIN(col) / MAX(col)", "the smallest / biggest value"]]),
   dict(t="sql", label="One aggregate over the whole table", text="SELECT COUNT(*) AS employees, MAX(salary) AS top_pay FROM employees;"),
   dict(t="h", text="GROUP BY: one result row per group"),
   dict(t="p", text="`GROUP BY department` puts all rows with the same department in one pile, and the aggregates are worked out for each pile. Every column in SELECT must be either in GROUP BY or inside an aggregate."),
   dict(t="sql", label="Headcount per department", text="SELECT department, COUNT(*) AS headcount\nFROM employees\nGROUP BY department;"),
   dict(t="sql", label="Average pay, rounded to a whole number", text="SELECT department, ROUND(AVG(salary)) AS average_pay\nFROM employees\nGROUP BY department;"),
   dict(t="h", text="WHERE or HAVING"),
   dict(t="p", text="`WHERE` filters rows before they are grouped. `HAVING` filters groups after the totals are worked out. Use WHERE for facts about single rows (status is shipped). Use HAVING for facts about the totals (more than 3 people)."),
   dict(t="sql", label="Only departments with more than three people", text="SELECT department, COUNT(*) AS headcount\nFROM employees\nGROUP BY department\nHAVING COUNT(*) > 3;"),
   dict(t="sql", label="WHERE first, then group: only shipped orders", text="SELECT customer_id, SUM(amount) AS total\nFROM orders\nWHERE status = 'shipped'\nGROUP BY customer_id;"),
   dict(t="callout", text="The full order of the words is: SELECT, FROM, JOIN, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT. The database does not run them in that order, but you must write them in it."),
   dict(t="warn", text="`COUNT(*)` counts rows. `COUNT(column)` counts only rows where that column is not NULL. They can give different numbers."),
   dict(t="sql", label="Joining and grouping together: total spent per customer", text="SELECT c.name, SUM(o.amount) AS total\nFROM customers c\nJOIN orders o ON o.customer_id = c.id\nGROUP BY c.name\nORDER BY total DESC;"),
  ],
  after=dict(text="Practise grouping and totals.", href="#/sql", button="Open the SQL practice list")),
]

PROBLEMS = []
def sp(lesson, id, title, diff, statement, solution, hints, count, ordered=False, tables=None):
    assert len(hints) == 4, id
    PROBLEMS.append(dict(id=id, lesson=lesson, title=title, difficulty=diff, statement=statement, solution=solution, hints=hints,
                         expect_count=count, ordered=ordered, tables=tables or ["employees"]))

# ---- SELECT and WHERE ----
sp("sql_select", "sql_all_employees", "Everything about employees", "Easy",
 ["Show every column and every row of the `employees` table."],
 "SELECT * FROM employees;",
 ["SELECT chooses columns and FROM chooses the table.", "The star * means all columns.", "Write SELECT, then the star, then FROM, then the table name.", "SELECT * FROM employees;"], 12)
sp("sql_select", "sql_customer_names", "Customer names", "Easy",
 ["Show only the `name` column of the `customers` table."],
 "SELECT name FROM customers;",
 ["Name the column instead of using a star.", "After SELECT, write the column name you want.", "SELECT the name column FROM the customers table.", "SELECT name FROM customers;"], 8, tables=["customers"])
sp("sql_select", "sql_sales_staff", "Sales team", "Easy",
 ["Show the `name` and `salary` of employees in the Sales department."],
 "SELECT name, salary FROM employees WHERE department = 'Sales';",
 ["WHERE keeps only rows that match a condition.", "Text values go in single quotes. A single = compares in SQL.", "SELECT the two columns, FROM employees, WHERE department equals Sales.", "SELECT name, salary FROM employees WHERE department = 'Sales';"], 3)
sp("sql_select", "sql_high_earners", "High earners", "Easy",
 ["Show the `name` of every employee who earns more than 70000."],
 "SELECT name FROM employees WHERE salary > 70000;",
 ["You need a comparison on the salary column.", "Numbers do not need quotes. The symbol > means greater than.", "SELECT name FROM employees, keeping rows WHERE salary is greater than 70000.", "SELECT name FROM employees WHERE salary > 70000;"], 4)
sp("sql_select", "sql_eng_under_80", "Engineers below 80000", "Medium",
 ["Show the `name` and `salary` of employees who work in Engineering and earn less than 80000."],
 "SELECT name, salary FROM employees WHERE department = 'Engineering' AND salary < 80000;",
 ["Two conditions must both be true.", "Join the two conditions with AND.", "WHERE department equals Engineering AND salary is less than 80000.", "SELECT name, salary FROM employees WHERE department = 'Engineering' AND salary < 80000;"], 2)
sp("sql_select", "sql_mouse_keyboard", "Mice and keyboards", "Easy",
 ["Show the `id` and `product` of every order for a Mouse or a Keyboard."],
 "SELECT id, product FROM orders WHERE product IN ('Mouse', 'Keyboard');",
 ["You could write two conditions with OR, but there is a shorter way.", "IN lets you list several allowed values in brackets.", "WHERE product IN, then the two product names in quotes inside brackets.", "SELECT id, product FROM orders WHERE product IN ('Mouse', 'Keyboard');"], 5, tables=["orders"])
sp("sql_select", "sql_name_ends_a", "Names ending in a", "Medium",
 ["Show the `name` of customers whose name ends with the letter a."],
 "SELECT name FROM customers WHERE name LIKE '%a';",
 ["LIKE compares text to a pattern.", "In a pattern, the percent sign % stands for any run of characters, including none.", "The pattern for ends with a is a percent sign followed by a, in quotes.", "SELECT name FROM customers WHERE name LIKE '%a';"], 2, tables=["customers"])
sp("sql_select", "sql_no_manager", "People without a manager", "Medium",
 ["Show the `name` of employees who have no manager. In the table this means `manager_id` is NULL."],
 "SELECT name FROM employees WHERE manager_id IS NULL;",
 ["NULL means a missing value.", "You cannot compare with = NULL. There is a special phrase for it.", "WHERE manager_id IS NULL.", "SELECT name FROM employees WHERE manager_id IS NULL;"], 4)
sp("sql_select", "sql_mid_orders", "Mid-priced orders", "Medium",
 ["Show the `id` and `amount` of orders with an amount from 100 to 300, including both 100 and 300."],
 "SELECT id, amount FROM orders WHERE amount BETWEEN 100 AND 300;",
 ["A range with both ends included has a short form.", "BETWEEN a AND b includes both a and b.", "WHERE amount BETWEEN 100 AND 300.", "SELECT id, amount FROM orders WHERE amount BETWEEN 100 AND 300;"], 5, tables=["orders"])
sp("sql_select", "sql_cities", "Which cities", "Medium",
 ["Show each city where at least one customer lives, once each, with no repeats."],
 "SELECT DISTINCT city FROM customers;",
 ["Several customers share a city, so a plain SELECT repeats it.", "DISTINCT removes repeated rows.", "SELECT DISTINCT, then the city column, FROM customers.", "SELECT DISTINCT city FROM customers;"], 4, tables=["customers"])

# ---- ORDER BY and LIMIT ----
sp("sql_order", "sql_pay_list", "Pay list", "Easy",
 ["Show the `name` and `salary` of every employee, with the highest salary first. If two people earn the same, put the name that comes first alphabetically first."],
 "SELECT name, salary FROM employees ORDER BY salary DESC, name;",
 ["ORDER BY sorts the result.", "DESC means biggest first. Add a second column after a comma to break ties.", "ORDER BY salary DESC, then name.", "SELECT name, salary FROM employees ORDER BY salary DESC, name;"], 12, ordered=True)
sp("sql_order", "sql_top3_paid", "Top three paid", "Easy",
 ["Show the `name` and `salary` of the three highest paid employees, highest first."],
 "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3;",
 ["Sort first, then keep only the top rows.", "LIMIT 3 keeps the first three rows, and it goes last in the query.", "ORDER BY salary DESC, then LIMIT 3.", "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3;"], 3, ordered=True)
sp("sql_order", "sql_dept_pay", "Pay inside each department", "Medium",
 ["Show `department`, `name` and `salary` for every employee. Sort by department A to Z. Inside a department, highest salary first, and for equal salaries the name A to Z."],
 "SELECT department, name, salary FROM employees ORDER BY department, salary DESC, name;",
 ["You need to sort by three things in order of importance.", "List them after ORDER BY, separated by commas. Each can have its own DESC.", "ORDER BY department, then salary DESC, then name.", "SELECT department, name, salary FROM employees ORDER BY department, salary DESC, name;"], 12, ordered=True)
sp("sql_order", "sql_newest_hires", "Newest two hires", "Medium",
 ["Show the `name` and `hire_year` of the two most recently hired employees, newest first."],
 "SELECT name, hire_year FROM employees ORDER BY hire_year DESC LIMIT 2;",
 ["Newest means the biggest hire_year.", "Sort so the biggest year comes first, then keep two rows.", "ORDER BY hire_year DESC LIMIT 2.", "SELECT name, hire_year FROM employees ORDER BY hire_year DESC LIMIT 2;"], 2, ordered=True)
sp("sql_order", "sql_latest_orders", "Latest orders", "Medium",
 ["Show the `id` and `order_date` of the three most recent orders, newest first. Dates are text written as YYYY-MM-DD, which sort correctly."],
 "SELECT id, order_date FROM orders ORDER BY order_date DESC LIMIT 3;",
 ["Dates in this form sort the same way as text.", "DESC puts the latest date first.", "ORDER BY order_date DESC, then LIMIT 3.", "SELECT id, order_date FROM orders ORDER BY order_date DESC LIMIT 3;"], 3, ordered=True, tables=["orders"])
sp("sql_order", "sql_low_balances", "Two lowest balances", "Medium",
 ["Show the `id` and `balance` of the two accounts with the lowest balance, lowest first."],
 "SELECT id, balance FROM accounts ORDER BY balance ASC LIMIT 2;",
 ["Lowest first is the normal sort direction.", "ASC is the default, so you may leave it out.", "ORDER BY balance, then LIMIT 2.", "SELECT id, balance FROM accounts ORDER BY balance ASC LIMIT 2;"], 2, ordered=True, tables=["accounts"])

# ---- JOIN ----
sp("sql_join", "sql_orders_with_names", "Orders with customer names", "Easy",
 ["Show the customer `name`, the order `product` and the order `amount` for every order."],
 "SELECT c.name, o.product, o.amount FROM orders o JOIN customers c ON o.customer_id = c.id;",
 ["The customer name lives in a different table from the order.", "JOIN customers ON the order's customer_id equals the customer's id.", "FROM orders, JOIN customers ON orders.customer_id = customers.id. Aliases o and c save typing.", "SELECT c.name, o.product, o.amount FROM orders o JOIN customers c ON o.customer_id = c.id;"], 14, tables=["orders", "customers"])
sp("sql_join", "sql_austin_orders", "Orders from Austin", "Medium",
 ["Show the customer `name` and the order `product` for orders placed by customers who live in Austin."],
 "SELECT c.name, o.product FROM orders o JOIN customers c ON o.customer_id = c.id WHERE c.city = 'Austin';",
 ["First join, then filter.", "After the JOIN, a WHERE can use columns from either table.", "Join orders to customers, then WHERE the customer's city equals Austin.", "SELECT c.name, o.product FROM orders o JOIN customers c ON o.customer_id = c.id WHERE c.city = 'Austin';"], 5, tables=["orders", "customers"])
sp("sql_join", "sql_customer_accounts", "Customers and their accounts", "Easy",
 ["Show the customer `name`, the account `type` and the account `balance` for every account."],
 "SELECT c.name, a.type, a.balance FROM accounts a JOIN customers c ON a.customer_id = c.id;",
 ["Accounts hold a customer_id.", "Join accounts to customers where the ids match.", "FROM accounts, JOIN customers ON accounts.customer_id = customers.id.", "SELECT c.name, a.type, a.balance FROM accounts a JOIN customers c ON a.customer_id = c.id;"], 8, tables=["accounts", "customers"])
sp("sql_join", "sql_never_ordered", "Customers who never ordered", "Hard",
 ["Show the `name` of every customer who has not placed any order."],
 "SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE o.id IS NULL;",
 ["An ordinary JOIN loses customers with no orders. You need a different kind.", "LEFT JOIN keeps every customer, and fills the order columns with NULL when there is no match.", "LEFT JOIN orders ON the ids match, then keep rows WHERE the order id IS NULL.", "SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE o.id IS NULL;"], 2, tables=["customers", "orders"])
sp("sql_join", "sql_returned_customers", "Customers with a return", "Medium",
 ["Show the `name` of each customer who has at least one order with status returned. List each name once."],
 "SELECT DISTINCT c.name FROM customers c JOIN orders o ON o.customer_id = c.id WHERE o.status = 'returned';",
 ["A customer with two returned orders would appear twice.", "DISTINCT removes repeated rows.", "Join customers to orders, keep status returned, and use DISTINCT.", "SELECT DISTINCT c.name FROM customers c JOIN orders o ON o.customer_id = c.id WHERE o.status = 'returned';"], 2, tables=["customers", "orders"])
sp("sql_join", "sql_employee_manager", "Employee and manager", "Hard",
 ["Show each employee's name as `employee` and their manager's name as `manager`. Leave out employees who have no manager."],
 "SELECT e.name AS employee, m.name AS manager FROM employees e JOIN employees m ON e.manager_id = m.id;",
 ["The manager is another row in the same table.", "Use the table twice with two different aliases, one for the employee and one for the manager.", "Join employees e to employees m where e.manager_id equals m.id.", "SELECT e.name AS employee, m.name AS manager FROM employees e JOIN employees m ON e.manager_id = m.id;"], 8)
sp("sql_join", "sql_savers_orders", "Orders of savers", "Hard",
 ["Show the customer `name` and the order `product` for customers who own a savings account. A customer who owns a savings account and has three orders should give three rows."],
 "SELECT c.name, o.product FROM customers c JOIN accounts a ON a.customer_id = c.id JOIN orders o ON o.customer_id = c.id WHERE a.type = 'savings';",
 ["You need three tables: customers, accounts and orders.", "A second JOIN can follow the first. Both join back to customers.", "customers JOIN accounts ON the ids match, JOIN orders ON the ids match, WHERE the account type equals savings.", "SELECT c.name, o.product FROM customers c JOIN accounts a ON a.customer_id = c.id JOIN orders o ON o.customer_id = c.id WHERE a.type = 'savings';"], 7, tables=["customers", "accounts", "orders"])

# ---- GROUP BY and HAVING ----
sp("sql_group", "sql_headcount", "Headcount per department", "Easy",
 ["Show each `department` and the number of employees in it, as a column called `headcount`."],
 "SELECT department, COUNT(*) AS headcount FROM employees GROUP BY department;",
 ["You want one row per department, not one per employee.", "GROUP BY department makes one pile per department. COUNT(*) counts rows in each pile.", "SELECT department and COUNT(*) AS headcount, FROM employees, GROUP BY department.", "SELECT department, COUNT(*) AS headcount FROM employees GROUP BY department;"], 4)
sp("sql_group", "sql_avg_pay", "Average pay", "Medium",
 ["Show each `department` and its average salary, rounded to the nearest whole number, as a column called `average_pay`."],
 "SELECT department, ROUND(AVG(salary)) AS average_pay FROM employees GROUP BY department;",
 ["AVG works out an average.", "ROUND(value) rounds to a whole number. Put AVG inside ROUND.", "SELECT department, ROUND(AVG(salary)) AS average_pay, FROM employees, GROUP BY department.", "SELECT department, ROUND(AVG(salary)) AS average_pay FROM employees GROUP BY department;"], 4)
sp("sql_group", "sql_big_departments", "Big departments", "Medium",
 ["Show each `department` that has more than 3 employees, with its `headcount`."],
 "SELECT department, COUNT(*) AS headcount FROM employees GROUP BY department HAVING COUNT(*) > 3;",
 ["WHERE cannot filter on a count, because the count does not exist until after grouping.", "HAVING filters groups, and it comes after GROUP BY.", "Group by department, then HAVING COUNT(*) greater than 3.", "SELECT department, COUNT(*) AS headcount FROM employees GROUP BY department HAVING COUNT(*) > 3;"], 1)
sp("sql_group", "sql_shipped_totals", "Shipped totals", "Medium",
 ["For orders with status shipped only, show each `customer_id` and the total of their `amount` as `total`."],
 "SELECT customer_id, SUM(amount) AS total FROM orders WHERE status = 'shipped' GROUP BY customer_id;",
 ["Filter the rows before you group them.", "WHERE comes before GROUP BY. SUM adds up a column.", "SELECT customer_id and SUM(amount) AS total, FROM orders, WHERE status equals shipped, GROUP BY customer_id.", "SELECT customer_id, SUM(amount) AS total FROM orders WHERE status = 'shipped' GROUP BY customer_id;"], 5, tables=["orders"])
sp("sql_group", "sql_big_spenders", "Big spenders", "Hard",
 ["Show the `name` and total spent (as `total`) for each customer whose orders add up to 1000 or more, counting all orders whatever their status."],
 "SELECT c.name, SUM(o.amount) AS total FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.name HAVING SUM(o.amount) >= 1000;",
 ["You need a join for the name, a group for the totals and a filter on the totals.", "Join customers to orders, GROUP BY the name, and use HAVING for the total test.", "SELECT name and SUM(amount) AS total, FROM customers JOIN orders, GROUP BY name, HAVING SUM(amount) at least 1000.", "SELECT c.name, SUM(o.amount) AS total FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.name HAVING SUM(o.amount) >= 1000;"], 3, tables=["customers", "orders"])
sp("sql_group", "sql_top_pay_dept", "Top pay in each department", "Medium",
 ["Show each `department` and its highest salary, as a column called `top_pay`."],
 "SELECT department, MAX(salary) AS top_pay FROM employees GROUP BY department;",
 ["MAX gives the biggest value in a group.", "Group by department.", "SELECT department and MAX(salary) AS top_pay, FROM employees, GROUP BY department.", "SELECT department, MAX(salary) AS top_pay FROM employees GROUP BY department;"], 4)
sp("sql_group", "sql_status_counts", "Orders by status", "Hard",
 ["Show each order `status` and the number of orders with that status, as `n`. Put the status with the most orders first. If two statuses have the same number, put the one that comes first alphabetically first."],
 "SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY n DESC, status;",
 ["Count per group, then sort the groups.", "ORDER BY comes after GROUP BY, and it can use the name you gave with AS.", "GROUP BY status, then ORDER BY n DESC, then status.", "SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY n DESC, status;"], 3, ordered=True, tables=["orders"])
sp("sql_group", "sql_rich_types", "Account types with a high average", "Hard",
 ["Show each account `type` whose average balance is above 5000, with the average rounded to 2 decimal places as `average_balance`."],
 "SELECT type, ROUND(AVG(balance), 2) AS average_balance FROM accounts GROUP BY type HAVING AVG(balance) > 5000;",
 ["The test is on an average, so it belongs in HAVING.", "ROUND takes a second value: how many decimal places to keep.", "Group by type. HAVING AVG(balance) greater than 5000. SELECT the rounded average.", "SELECT type, ROUND(AVG(balance), 2) AS average_balance FROM accounts GROUP BY type HAVING AVG(balance) > 5000;"], 1, tables=["accounts"])
sp("sql_group", "sql_repeat_buyers", "Repeat buyers", "Hard",
 ["Show the `name` of each customer with at least 3 orders, and their number of orders as `n`."],
 "SELECT c.name, COUNT(*) AS n FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.name HAVING COUNT(*) >= 3;",
 ["You need names from customers and a count from orders.", "Join, group by the name, and filter the count with HAVING.", "Join customers to orders. GROUP BY name. HAVING COUNT(*) at least 3.", "SELECT c.name, COUNT(*) AS n FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.name HAVING COUNT(*) >= 3;"], 2, tables=["customers", "orders"])

# Work out the expected rows by running each solution.
def _db():
    con = sqlite3.connect(':memory:')
    for t in TABLES.values(): con.executescript(t['create'])
    return con
_con = _db()
for _p in PROBLEMS:
    _cur = _con.execute(_p['solution'])
    _p['columns'] = [d[0] for d in _cur.description]
    _p['expected'] = [list(r) for r in _cur.fetchall()]
    assert len(_p['expected']) == _p['expect_count'], (_p['id'], len(_p['expected']), _p['expect_count'])

FILES = {"sql_tables.json": TABLES, "sql_problems.json": PROBLEMS}
