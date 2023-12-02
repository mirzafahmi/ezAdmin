# ezAdmin: Admin Made Effortless


## Table of Contents
- [ezAdmin: Admin Made Effortless](#ezadmin-admin-made-effortless)
  - [Table of Contents](#table-of-contents)
  - [General Info](#general-info)
  - [Key Objectives:](#key-objectives)
  - [Setup](#setup)
  - [How to Setup the webapps](#how-to-setup-the-webapps)
    - [Guideline to Install (CMD):](#guideline-to-install-cmd)
    - [Guideline to runserver:](#guideline-to-runserver)
      - [Development server (Localhost):](#development-server-localhost)
      - [Wifi host server:](#wifi-host-server)
  - [What is ezAdmin?](#what-is-ezadmin)
    - [Database overview diagram](#database-overview-diagram)
    - [Apps list](#apps-list)
      - [Store App](#store-app)
      - [Production App](#production-app)
      - [Purchasing App](#purchasing-app)
      - [Misc App](#misc-app)
      - [Office App](#office-app)
  - [Known bug/issue to fix:](#known-bugissue-to-fix)
  - [To-do/add-on features](#to-doadd-on-features)


## General Info

ezAdmin is a comprehensive web-based solution designed to streamline administrative tasks, minimize manual workload, automate repetitive processes, and create a centralized management system for your organization. This powerful tool is engineered with the aim of simplifying and enhancing the overall administrative experience, enabling your team to focus on more strategic and value-added activities.


## Key Objectives:

1. Efficiency Enhancement: ezAdmin aims to optimize the efficiency of administrative operations by automating routine tasks, reducing human errors, and improving data accuracy.

2. Centralized Management: The system centralizes various administrative functions, including inventory management, document generation, and data analysis, providing a single platform for all your administrative needs.

3. Workload Reduction: By automating mundane and time-consuming tasks, ezAdmin helps reduce the workload on administrative staff, allowing them to allocate more time to critical tasks.

4. Data-Driven Decision Making: Through advanced data analysis and visualization tools, ezAdmin empowers your organization to make informed, data-driven decisions based on real-time information.

5. User-Friendly Interface: The user-friendly interface ensures that employees across different departments can easily navigate and utilize the system, enhancing overall usability.

6. Scalability: ezAdmin is designed to adapt and scale with your organization's evolving administrative requirements, ensuring it remains a valuable asset as your company grows.


## Setup 

## How to Setup the webapps

### Guideline to Install (CMD):

1. Install python and pip that required to run this project. Download it at the specified link below:
      1. Python: https://www.python.org/downloads/ (Note: this project build on Python 3.11.5)
      2. Pip: https://bootstrap.pypa.io/get-pip.py (Note: this project build on pip 23.3.1)
         1. Change directory to the installed python directory, paste the `get-pip.py` file, open a terminal/command prompt at that directory, and run: <br>
               ```
               python get-pip.py
               ```
           1. or follow this guideline at https://www.geeksforgeeks.org/how-to-install-pip-on-windows/

2. Install virtual enviroment package by this command: <br>
   ```
   pip install virtualenv
   ``` 
   <br>

3. Create virtual enviroment: <br>
   ```
   python -m venv myenv
   ``` 
   <br>

4. To install the required packages for this project, run the following command in your terminal: <br>
    ```
    pip install -r requirements.txt
    ```

### Guideline to runserver:

#### Development server (Localhost):

1. Activate virtual enviroment by run this command: <br>
   ```
    myenv\scripts\activate.bat
    ```
    <br> 
2. Change to the project directory where your Django project is located. You should be in the same directory as ```manage.py``` by running this code.<br>
    ```
    cd ezAdmin
    ```
    <br>
3. Once you're in the project directory (run `dir` command in cmd to make sure in same directory with `manage.py`), you can start the development server using the following command:<br>
    ```
    python manage.py runserver
    ```
    <br>
4. This command will launch the Django development server, and you can access your project in a web browser at the specified address (usually http://127.0.0.1:8000/). Click or copy and paste it at browser and it will open the landing page of the webapp. `Register/Login` if necessary.


#### Wifi host server:

1. Run ```runserver_local_wifi.bat``` and let the batch file configure the settings.
2. Once server is running, you can access this project in a web browser at the specified address (usually start with http://.../../..). Click or copy and paste it at browser and it will open the landing page of the webapp. `Register/Login` if necessary.


## What is ezAdmin?

### Database overview diagram

Attached here is the overview of the DB for this project: <br>
<br> ![ezAdmin-db](/ezAdmin/static/ezAdmin_DB.png)

### Apps list

This project consist of 5 main major apps which are: <br>

   1. Store App <br>
   2. Production App <br>
   3. Purchasing App <br>
   4. Misc App <br>
   5. Office App <br>

#### Store App
   
For Store app, it consist of 2 models which are:

1. **Brand Model:** <br>
     Brand have Create, Read, Update, Delete (CRUD) operations. This `Brand` model have field such as brand name and company name that will be used through out this webapp.
     <br>

2. **Product Model:** <br>
     Product have Create, Read, Update, Delete (CRUD) operations. This `Product` model have field such as product name, item code, packing and etc. that will be used through out this webapp.  
     <br>

#### Production App

For Production app, it consist of 5 models which are:

1. **Raw Material Identifier:** <br>
   Raw Material Identifier have Create, Read, Update, Delete (CRUD) operations. This `Raw Material Identifier` model have field such as parent item code that origin from parent base item code that will act as identifier and be used through out this webapp. For examples if you have product line such as PRODUCT-1-VAR-1, PRODUCT-1-VAR-2, it identifier would be **PRODUCT-1** or like in real life example, Perodua have product line of AXIA-E, AXIA-AV, AXIA-SE, its identifier would be **AXIA** (Note that this example is for educational examples only).
   <br>

2. **Raw Material Component:** <br>
   Raw Material Component have Create, Read, Update, Delete (CRUD) operations. This `Raw Material Component` model have field such as component or specification for specific `Raw Material Identifier` that will be used through out this webapp. Each of this data have data constraint to avoid the duplication of same combination between `Raw Material Identifier`, component and spec data/field of `Raw Material Component`.
   <br>

3. **Raw Material BOM Component:** <br>
   Raw Material BOM Component have Create, Read, Update, Delete (CRUD) operations. This `Raw Material BOM Component` model have field such as quantity used or specification of for specific `Product` and `Raw Material Component` that will be used through out this webapp. Each of this data have data constraint to avoid the duplication of same combination between `Product` and `Raw Material Component`.
   <br>

4. **Raw Material Inventory:** <br>
   Raw Material Inventory have Create, Read, Update, Delete (CRUD) operations. This `Raw Material Inventory` model have field such as quantity, lot number, exp date and etc. that will be used through out this webapp. 
   <br>
   <br>
   This subcomponent has `Raw Material Inventory List (Identifier Based) Page` that will list all added identifier. It also have button features that will shortcut to add `Raw Material Identifier` and feature to generate available raw material with its detail up to certain date. 
   <br>
   <br>
   If click at any card's button of the corresponding `Raw Material Identifier`, it will redirect to `Raw Material Inventory List  Identifier Based Page` that will list all added component for specific identifier. It also have shortcut button to add component of related `Raw Material Identifier`. 
   <br>
   <br>
   If click at any card's button of the corresponding `Raw Material Component`, it will redirect to `Identifier Raw Material Inventory List` for the corrensponding component. This page consist of details of that specific component of specific identifier such as quantity, lot number, and etc. And it also have modals that can be toggle to have quick access of related purchasing documents.
   <br>

5. **Production Log:** <br>
   Production Log have Create, Read, Update, Delete (CRUD) operations. This `Production Log` model data have details such as finished product lot number, exp date, details of raw material used and etc that will be used through out this webapp. Once the log is generated or deleted, it will also log that operation in the `Raw Material Inventory` for the selected `Product` when creating the `Production Log`. For the mean time, update operation still in development. For now, it only able to update the **lot number** and **exp date** of that log.
   <br>

#### Purchasing App

For Purchasing app, it consist of 2 models which are:

1. **Supplier:** <br>
   Supplier have Create, Read, Update, Delete (CRUD) operations. This `Supplier` model have field such as company name, address and etc that will be used through out this webapp.  
   <br>

2. **Purchasing Document:** <br>
   Purchasing Document have Create, Read, Update, Delete (CRUD) operations. This `Purchasing Document` model have field such as `Supplier`, all purchasing document and etc. that will be used through out this webapp. This subcomponent also able to store/upload and retrieve/dowload the purchasing documents for ease of query in future usage.
   <br>

#### Misc App

For Misc app, it consist of 2 models which are:

1. **Unit of measurement (UOM):** <br>
   Unit of measurement (UOM) have Create, Read, Update, Delete (CRUD) operations. This `Unit of measurement (UOM)` model have field such as UOM that will be used through out this webapp. 
   <br>

2. **Currency:** <br>
   Currency have Create, Read, Update, Delete (CRUD) operations. This `Currency` model have field such as currency and currency code that will be used through out this webapp.  
   <br>

#### Office App

For Office app, it consist of 7 models which are:

1. **Electronic User Location:** <br>
    Electronic User Location have Create, Read, Update, Delete (CRUD) operations. This `Electronic User Location` model data have details such as location of the careholder, name of careholder and phone number of careholder that will be used through out this webapp. 
   <br>

2. **Electronic User:** <br>
   Electronic User have Create, Read, Update, Delete (CRUD) operations. This `Electronic User` model data have details such as user name, user position and user location from `Electronic User Location` model that will be used through out this webapp.  
   <br>

3. **Electronic Brand:** <br>
   Electronic Brand have Create, Read, Update, Delete (CRUD) operations. This `Electronic Brand` model data have details such as brand name that will be used through out this webapp.  
   <br>

4. **Electronic Model:** <br>
   Electronic Model have Create, Read, Update, Delete (CRUD) operations. This `Electronic Model` model data have details such as brand from `Electronic Brand` model and model name that will be used through out this webapp.  
   <br>
   
5. **Electronic Purchasing Document:** <br>
   Electronic Purchasing Document have Create, Read, Update, Delete (CRUD) operations. This `Electronic Purchasing Document` model data have details such as supplier, PO details and invoice details that will be used through out this webapp. It also have features to store the PO document or Invoice document in the form to ease the reference and query in future.
   <br>

6. **Electronic Inventory:** <br>
   Electronic Inventory have Create, Read, Update, Delete (CRUD) operations. This `Electronic Inventory` model data have details such as electronic item, serial number, price per unit and etc. that will be used through out this webapp. 
   <br>
   <br>
   *Status* field in this model inter-connected with *Transaction Type* field in `Electronic Transaction` that would reflect each other. If that `Electronic Inventory`'s data/instance of *Status* show **Idle**, it mean that there is no instance of `Electronic Transaction` currently **Checked-Out** that `Electronic Inventory` instance and vice versa.
   <br>

7. **Electronic Transaction:** <br>
   Electronic Transaction have Create, Read, Update, Delete (CRUD) operations. This `Electronic Transaction` model data have details such as current user, electronic item details, transaction type and etc that will be used through out this webapp.
   <br>
   <br>
   It also have features to store the initial agreement document or return agreement document in the form to ease the reference and query in future. *Transaction Type* field in this model is inter-connected with *Status* field in `Electronic Inventory` that would reflect each other. If `Electronic Transaction`'s data/instance of *Transaction Type* show **Check-Out**, it mean that the selected electronic item in that instance of `Electronic Transaction` will reflect it as **In-Use** in *Status* field of `Electronic Inventory` model and vice versa.
   <br>


## Known bug/issue to fix:

1. Finalize update view for the production log in production app to have same function as create view.
2. Add validation function for all validate button.


## To-do/add-on features

1. Expand store apps
   <br>
   <br>
   <label for="file">Progress:  </label> [](https://geps.dev/progress/000)

2. Optimize the layout for mobile user
   <br>
   <br>
   <label for="file">Progress:  </label> [](https://geps.dev/progress/000)

3. Create Sales apps
   <br>
   <br>
   <label for="file">Progress:  </label> [](https://geps.dev/progress/000)

4. Make the project/webapp general that able to host multiple company simultaneously
   <br>
   <br>
   <label for="file">Progress:  </label> [](https://geps.dev/progress/000)
