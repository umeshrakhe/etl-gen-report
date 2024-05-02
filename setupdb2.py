import sqlite3
import cx_Oracle

# Function to create tables and insert sample data
def create_sqlite_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('metadata.db')
    c = conn.cursor()

    # Create Data_Sources table
    c.execute('''CREATE TABLE IF NOT EXISTS Data_Sources (
                    data_source_id INTEGER PRIMARY KEY,
                    data_source_name TEXT,
                    data_source_type TEXT,
                    data_source_description TEXT
                 )''')

    # Insert sample data into Data_Sources table
    c.execute("INSERT INTO Data_Sources (data_source_name, data_source_type, data_source_description) VALUES (?, ?, ?)",
              ('Sales_Data', 'Table', 'Contains sales data for the past year'))
    c.execute("INSERT INTO Data_Sources (data_source_name, data_source_type, data_source_description) VALUES (?, ?, ?)",
              ('Customer_Records', 'File', 'CSV file containing customer records'))

    # Create Transformations table
    c.execute('''CREATE TABLE IF NOT EXISTS Transformations (
                    transformation_id INTEGER PRIMARY KEY,
                    transformation_name TEXT,
                    transformation_description TEXT
                 )''')

    # Insert sample data into Transformations table
    c.execute("INSERT INTO Transformations (transformation_name, transformation_description) VALUES (?, ?)",
              ('Data Cleansing', 'Remove duplicates and fill missing values'))
    c.execute("INSERT INTO Transformations (transformation_name, transformation_description) VALUES (?, ?)",
              ('Data Aggregation', 'Aggregate sales data by month'))

    # Create Mappings table
    c.execute('''CREATE TABLE IF NOT EXISTS Mappings (
                    mapping_id INTEGER PRIMARY KEY,
                    source_field TEXT,
                    target_field TEXT,
                    transformation_id INTEGER,
                    data_source_id INTEGER,
                    FOREIGN KEY (transformation_id) REFERENCES Transformations(transformation_id),
                    FOREIGN KEY (data_source_id) REFERENCES Data_Sources(data_source_id)
                 )''')

    # Insert sample data into Mappings table
    c.execute("INSERT INTO Mappings (source_field, target_field, transformation_id, data_source_id) VALUES (?, ?, ?, ?)",
              ('product_id', 'id', 1, 1))
    c.execute("INSERT INTO Mappings (source_field, target_field, transformation_id, data_source_id) VALUES (?, ?, ?, ?)",
              ('customer_name', 'name', 1, 2))

    # Create Business_Rules table
    c.execute('''CREATE TABLE IF NOT EXISTS Business_Rules (
                    rule_id INTEGER PRIMARY KEY,
                    rule_name TEXT,
                    rule_description TEXT
                 )''')

    # Insert sample data into Business_Rules table
    c.execute("INSERT INTO Business_Rules (rule_name, rule_description) VALUES (?, ?)",
              ('Customer Eligibility', 'Customers with a purchase history of more than $1000 are eligible for discounts'))
    c.execute("INSERT INTO Business_Rules (rule_name, rule_description) VALUES (?, ?)",
              ('Product Availability', 'Products with stock quantity less than 10 are considered low availability'))

    # Create Report_Definitions table
    c.execute('''CREATE TABLE IF NOT EXISTS Report_Definitions (
                    report_id INTEGER PRIMARY KEY,
                    report_name TEXT,
                    report_description TEXT
                 )''')

    # Insert sample data into Report_Definitions table
    c.execute("INSERT INTO Report_Definitions (report_name, report_description) VALUES (?, ?)",
              ('Sales Report', 'Monthly report summarizing sales performance'))
    c.execute("INSERT INTO Report_Definitions (report_name, report_description) VALUES (?, ?)",
              ('Customer Report', 'List of customers with contact information'))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Call the function to create the database
#create_sqlite_database()

# Function to create tables and insert sample data
def create_oracle_database():
    # Connect to Oracle database
    conn = cx_Oracle.connect('username/password@hostname:port/service_name')

    # Create a cursor
    c = conn.cursor()

    # Create Data_Sources table
    c.execute('''CREATE TABLE Data_Sources (
                    data_source_id NUMBER PRIMARY KEY,
                    data_source_name VARCHAR2(255),
                    data_source_type VARCHAR2(100),
                    data_source_description VARCHAR2(1000)
                 )''')

    # Insert sample data into Data_Sources table
    c.execute("INSERT INTO Data_Sources (data_source_id, data_source_name, data_source_type, data_source_description) VALUES (1, 'Sales_Data', 'Table', 'Contains sales data for the past year')")
    c.execute("INSERT INTO Data_Sources (data_source_id, data_source_name, data_source_type, data_source_description) VALUES (2, 'Customer_Records', 'File', 'CSV file containing customer records')")

    # Create Transformations table
    c.execute('''CREATE TABLE Transformations (
                    transformation_id NUMBER PRIMARY KEY,
                    transformation_name VARCHAR2(255),
                    transformation_description VARCHAR2(1000)
                 )''')

    # Insert sample data into Transformations table
    c.execute("INSERT INTO Transformations (transformation_id, transformation_name, transformation_description) VALUES (1, 'Data Cleansing', 'Remove duplicates and fill missing values')")
    c.execute("INSERT INTO Transformations (transformation_id, transformation_name, transformation_description) VALUES (2, 'Data Aggregation', 'Aggregate sales data by month')")

    # Create Mappings table
    c.execute('''CREATE TABLE Mappings (
                    mapping_id NUMBER PRIMARY KEY,
                    source_field VARCHAR2(255),
                    target_field VARCHAR2(255),
                    transformation_id NUMBER,
                    data_source_id NUMBER,
                    CONSTRAINT fk_transformation FOREIGN KEY (transformation_id) REFERENCES Transformations(transformation_id),
                    CONSTRAINT fk_data_source FOREIGN KEY (data_source_id) REFERENCES Data_Sources(data_source_id)
                 )''')

    # Insert sample data into Mappings table
    c.execute("INSERT INTO Mappings (mapping_id, source_field, target_field, transformation_id, data_source_id) VALUES (1, 'product_id', 'id', 1, 1)")
    c.execute("INSERT INTO Mappings (mapping_id, source_field, target_field, transformation_id, data_source_id) VALUES (2, 'customer_name', 'name', 1, 2)")

    # Create Business_Rules table
    c.execute('''CREATE TABLE Business_Rules (
                    rule_id NUMBER PRIMARY KEY,
                    rule_name VARCHAR2(255),
                    rule_description VARCHAR2(1000)
                 )''')

    # Insert sample data into Business_Rules table
    c.execute("INSERT INTO Business_Rules (rule_id, rule_name, rule_description) VALUES (1, 'Customer Eligibility', 'Customers with a purchase history of more than $1000 are eligible for discounts')")
    c.execute("INSERT INTO Business_Rules (rule_id, rule_name, rule_description) VALUES (2, 'Product Availability', 'Products with stock quantity less than 10 are considered low availability')")

    # Create Report_Definitions table
    c.execute('''CREATE TABLE Report_Definitions (
                    report_id NUMBER PRIMARY KEY,
                    report_name VARCHAR2(255),
                    report_description VARCHAR2(1000)
                 )''')

    # Insert sample data into Report_Definitions table
    c.execute("INSERT INTO Report_Definitions (report_id, report_name, report_description) VALUES (1, 'Sales Report', 'Monthly report summarizing sales performance')")
    c.execute("INSERT INTO Report_Definitions (report_id, report_name, report_description) VALUES (2, 'Customer Report', 'List of customers with contact information')")

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Call the function to create the database
#create_database()
#Make sure to replace `'username/password@hostname:port/service_name'` with your actual Oracle connection string. Additionally, you may need to install the cx_Oracle library if you haven't already done so.