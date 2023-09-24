# ezAdmin: Admin Made Effortless


## Table of Contents
- [ezAdmin: Admin Made Effortless](#ezadmin-admin-made-effortless)
  - [Table of Contents](#table-of-contents)
  - [General Info](#general-info)
  - [Key Objectives:](#key-objectives)
  - [Packages Involved](#packages-involved)
  - [Setup](#setup)
    - [Guideline to Install:](#guideline-to-install)
    - [Guideline to runserver:](#guideline-to-runserver)
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

## Packages Involved

This project depend on:

* asgiref             3.7.2
* crispy-bootstrap5   0.7
* Django              4.2.4
* django-crispy-forms 2.0
* numpy               1.25.2
* pandas              2.1.0
* pathlib             1.0.1
* Pillow              10.0.0
* pip                 23.2.1
* python-dateutil     2.8.2
* pytz                2023.3
* setuptools          65.5.0
* six                 1.16.0
* sqlparse            0.4.4
* tzdata              2023.3

## Setup 

### Guideline to Install:

1. To install the required packages for this project, run the following command in your terminal:

    ```bash
    pip install -r requirements.txt
    ```

### Guideline to runserver:

1. Change to the project directory
Navigate to the directory where your Django project is located. You should be in the same directory as `manage.py` by running this code.
    ```bash
    cd ezadmin
    ```
2. Once you're in the project directory, you can start the development server using the following command:
    ```bash
    python manage.py runserver
    ```
3. This command will launch the Django development server, and you can access your project in a web browser at the specified address (usually http://127.0.0.1:8000/). Click it and it will open the landing page of the server. `Register/Login` if necessary.

## To-do/add-on features

1. User Registration/Log-In function and page
  
    <label for="file">Progress:  </label> ![](https://geps.dev/progress/100)

2. Customer, Quotation and order execution fuctionality and page
  
    <label for="file">Progress:  </label> ![](https://geps.dev/progress/100)

3. Product and inventory registration and CRUD function
  
    <label for="file">Progress:  </label> ![](https://geps.dev/progress/100)

4. Modify the models and server functionality based on new plan
  
    <label for="file">Progress:  </label> ![](https://geps.dev/progress/20)

5. Analyze and create visualization page for forecasting
  
    <label for="file">Progress:  </label> ![](https://geps.dev/progress/0)

6. Auto generate ISO/GDPMD-related documentation based on system data
  
    <label for="file">Progress:  </label> ![](https://geps.dev/progress/0)

7. Create inventory for raw material functionality and page
  
    <label for="file">Progress:  </label> ![](https://geps.dev/progress/0)

8. Create production log functionality, page and connection with finished goods model
  
    <label for="file">Progress:  </label> ![](https://geps.dev/progress/0)