The Banking Service Application represents a comprehensive Python-based solution designed to emulate the functionality of a banking system. In the modern era, where digitalization plays a pivotal role in financial transactions and management, this application serves as a versatile tool for both customers and administrators alike. By leveraging Python's flexibility and simplicity, the Amatya Banking Service offers a seamless user experience while incorporating essential features for secure and efficient banking operations. The primary objective of the Amatya Banking Service Application is to provide a convenient platform for customers to manage their accounts and conduct financial transactions securely. From depositing funds to generating account statements, customers can execute a wide range of operations conveniently from the comfort of their homes or offices. Furthermore, administrators are equipped with powerful tools to oversee customer accounts, manage staff details, and ensure the smooth functioning of the banking system.

Assumptions
1. Customer Information Storage:
• Customer information such as account ID, name, account type, password, and balance are stored in 
separate text files (customer_info.txt).
• Each line in the customer information file represents a customer's data, with fields separated by commas.
2. Admin and Staff Information:
• Administrative and staff information are stored in separate text files (admin_info.txt and staff_info.txt
respectively).
• Similar to customer information, each line in these files represents an admin or staff member's data, with 
fields separated by commas.
3. Transaction Logging:
• Transaction history is recorded in a text file (transaction_history.txt), with each transaction logged in a 
separate line.
• Each transaction entry includes details such as timestamp, account ID, transaction type (deposit or 
withdrawal), and transaction amount. 
4. Minimum Balance Requirements:
• Minimum balance requirements are enforced for both savings and current accounts.
• Savings accounts must maintain a minimum balance of 100, while current accounts must maintain a 
minimum balance of 500. 
5. Security Measures:
• Customers must log in using their account ID and password to access their accounts. 
• Passwords are stored securely and being saved to the customer information file.
6. User Interaction:
• Users interact with the application through a command-line interface (CLI).
• Menus are displayed for customers, admins, and staff to perform various operations such as login, 
registration, and account managemen
