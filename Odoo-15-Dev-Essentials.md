# Odoo 15

## Table of Contents
**Intro**
1. Quickstart
2. Preparing the Dev Environment
3. Your First Odoo Application
4. Extending Modules

**Models**
5. Importing, Exporting, and Module Data
6. Models - Structuring the Application Data

**Business Logic**
7. Recordsets - Working with Model Data
8. Business Logic - Supporting Business Processes
9. External API - Integrating with Other Systems

**Views**
10. Backend Views - Designing the User Interface
11. Kanban Views and Client-Side QWeb
12. Creating Printable PDF Reports with Serer-Side QWeb
13. Creating Web and Portal Frontend Features

**Deployment and Maintenance**
14. Understanding Odoo Built-In Models
15. Deploying and Maintaining Production Instances13. Creating Web and Portal Frontend Features

## Preface

**Odoo** is a full-featured open source platform to build applications. Core framework with a suite of integrated applications for businesses including CRM, Sales, Inventory and Accounting. Built with extensibility and modification in mind. Odoo makes it easy to build **UI** such as kanban view, as well as calendar and graph. It is useful to think about application by considering the tiers involved:
+ **Data Tier:** This tier is implemented through models. *Contact/Partner* model and access control security.
+ **Business Logic Tier:** This is implemented through **Python** automation code. Allows basic CRUD handled by the framework.
+ **Presentation Tier:** This teir is implemented through views. *List* view (to browse existing records) and *form* view (to zoom in to see a record and see all of its details).
