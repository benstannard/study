# Odoo

[Odoo Community Association (OCA)](https://github.com/oca)
+ Version 15, the last three stable versions are supported
+ Odoo databases are incompatible between its major versions! The same is true for **addon modules**.

## Things to remember
+ ` odoo -u --upgrade --test-enable` `odoo` will look for tests/ subdirectory
+ While developing around `<data noupdate="1">` one workaround is to reinstall the module using `-i` instead of upgrading with `-u`
+ Odoo modles are kept in a *central registry*, available throught the environment object, which is usually accessed using `self.env`, `self.env["mymodel"]`
+ Model names must be **globally unique** as they are they key to accessing the model registry. Good practice to use the first word of the application as the first word in the models name as a **prefix**. Model Names should use the *singular form* library.book
+ Access privileges are granded to security groups, and users are assigned security groups. Access-secuirty-related files are kept in the `security/` module subdirectory. Security groups are organized in the same **categories** used for addon modules. `base.module_category_services_mymodule`. `manager` group will inherit from `user` privileges. Add the security definitions before the menu and view in `"data"` key in `__manifest__` (p86)

The `Book` model has the following relationships: (p189)
+ Each book can have one publisher, and each publisher can have many books. From the book's point of view, this is a *many-to-one relationship.* It is implemented in the db as an integer field, holding the ID of the related publisher record, and a database foreign key in it, enforcing referential integrity.

+ **Web Controllers** are the server side components responsible for when an Odoo web path is accessed, usually triggering the rendering of a web page. (p442)


## Table of Contents
**Intro**
1. Quickstart
2. Preparing the Dev Environment
3. Your First Odoo Application
4. Extending Modules
5. Importing, Exporting, and Module Data **Models**
6. Models - Structuring the Application Data **Models**
7. Recordsets - Working with Model Data **Business Logic**
8. Business Logic - Supporting Business Processes **Business Logic**
9. External API - Integrating with Other Systems **Business Logic**
10. Backend Views - Designing the User Interface **Views**
11. Kanban Views and Client-Side QWeb **Views**
12. Creating Printable PDF Reports with Serer-Side QWeb **Views**
13. Creating Web and Portal Frontend Features **Views**
14. Understanding Odoo Built-In Models **Deployment and Maintenance**
15. Deploying and Maintaining Production Instances13. Creating Web and Portal Frontend Features **Deployment and Maintenance**

## Preface

**Odoo** is a full-featured open source platform to build applications. Core framework with a suite of integrated applications for businesses including CRM, Sales, Inventory and Accounting. Built with extensibility and modification in mind. Odoo makes it easy to build **UI** such as kanban view, as well as calendar and graph. It is useful to think about application by considering the tiers involved:

+ **Presentation Tier:** This tier is implemented through views. *List* view (to browse existing records) and *form* view (to zoom in to see a record and see all of its details).
+ **Business Logic Tier:** This is implemented through **Python** automation code. Allows basic CRUD handled by the framework.
+ **Data Tier:** Stores data in a database or filesystem. This tier is implemented through models. *Contact/Partner* model and access control security.

The ability to select a list of people that will be working on the task, so we need a model to represent **people**. Odoo includes the *Contact* model with technical name of `res.partner` to use for individual people, companies, and addresses.

### ORM, RPC, web clients, XML and QWeb
Odoo relies on its **Object Relational Mapping (ORM)** enging as the interface between the apps and the database. CRUD basic operations are implemented by `create()`, `search()`, `write()`, and `unlink()` model methods and might implement default values or some other automation.  

*Presentation* tier is responsible for presenting data and interacting with the user. It is implemented by the client part of the software and uses **remote procedure calls (RPCs)** to the Odoo service, running the ORM engine and business logic.  

Odoo provides a web client out of the box and supports logins, navigation menus, data lists, and forms. The website framework is also available to use a public frontend for external users. It provides CMS features, allowing us to create both static and dynamic webpages. The website framework uses **controller** components for the code implementing the presentation-specific logic, keeping it seperate from the model's intrinsic logic. The page rendering uses **QWeb** as the templatign engine. These are **XML documents** that contain HTML markup plus XML QWeb tags for operations suck as loops, conditions, or calls to include other templates.  

### Understanding view types

- Form view
- Kanban view, the initial view type for Contacts, showing the record in data cards. Kanban can also group the cards in columns
- List view (sometimes referred to as the *tree view*) displays the records as a list.
- Search view, controls the behavior of the search box on the top-right of Kanban and List views, as well as the buttons under it: **Filters** and **Group By**

```
<tree>
    <field name="x_name />
</tree>

<form>
    <group>
        <field name="x_name />
        ...
    </group>
</form>

<search>
    <filter .... />
</search>
```

Other notes on views:
+ The base view is one with an empty **Inherired View** field. View types can have multiple base views
+ Views also have a **Sequence** field. A base view with the lowest **Sequence** number is the one displayed by default.
+ **Window Actions**, which are used in menu items, can specify a particular base view to use. If no specific view is defined, the one with the lowest sequence will be used.

### Understanding window actions

Menus can be a tree of menu items with a parent/child relations. There are several *action types* available, the most important are `window`, `report`, and `server`.

### Configuring access control and security groups

A user will only be able to use the features they were granted access to. Access security is defined using *user groups*. *Groups*, which are sometimes called **access control lists (ACLs)** define the access permissions for the models. Users belong to groups. Access control is based on *groups*. A **security group** is a given access privileges on models and this will determine menu items available to the users belonging to that group.
+ For more fine-grained control, we can also give access to specific menu items, views, fields, and even data records by using record rules.
+ Security Groups, there are usually at least two: `User` with permissions for daily tasks, and `Manager`, with permissions for performing all configurations for that app.

## Your First Odoo Application
Developing in Odoo usually means creating our own modules. Odoo follows a **Model-View-Controller MVC** like architecture. Rough outline:
1. Create new `addon` module
2. Create a new application
3. Adding automated tests
4. Implementing the model layer
5. Setting up access security
6. Implementing the backend view layer
7. Implementing the business logic layer
7. Implementing the website **user interface (UI)**

### Step 1 - creating a new addon module
An addon module is a directory containing files that implement some Odoo features. It can add new features or modify existing ones. The `addon` module directory must contain a manifest file named `__manifest__.py`, containing a dictionary {}. A non-module addon is expencted to depend on a app, adding or extending features to it. `__manifest__.py` keys:
```
{
    'name':
    'summary':
    'author':
    'license':
    'website': URL # with documentaion and issue tracker for bugs
    'version': 15.0.1.0.0 # targer Odoo major version
    'depends': base # if no dependancies otherwise will trigger installation
    'application': True # flag whether the modules should be feature as an app in the app list.
    'category': "Accounting" # "Sales" etc; find a category for app
    'auto_install': # can be set to true if it is a glue between apps

    "data": [
        "views/library_menu.xml",   # data files loaded by module upon installation or upgrade
    ],
}
```

#### Module Directory, fyi `scaffold` command

```
library_app/
├── __init__.py
├── __manifest__.py
├── controllers
│   ├── __init__.py
│   └── controllers.py
├── demo
│   └── demo.xml
├── models
│   ├── __init__.py
│   └── models.py
├── security
│   └── ir.model.access.csv
└── views
    ├── templates.xml
    └── views.xml
```

The `__init__.py` module file should trigger the import of all the module's Python Files.
```
# __init__.py
from . import controllers
from . import models
```

### Step 2 - Creating a new applications

A app is expected to have the following:
+ An icon, to be presented in the app list added to `static/description/` subdirectory
+ A top-level menu item, under which all the app's menu items will be placed. These are view components added using XML data files
+ Security Groups for the app so it can be enabled for users that need it, and where access security will be set An icon, to be presented in the app list

#### Adding a top menu item

`<menuitem>` element is an instruction to write a record on the `ir.ui.menu` model, where Odoo menu items are stored. The `id` attribute is also known as an **XML ID** and is used to uniquely identify each data element, providing a way for other elements to reference it. **submenu** added later will need to reference their parent menu item. Module does not know about this new XML files yet, needs to be added to `__manifest__.py`. To load these configurations into our Odoo database, we need to upgrade the module.

```
# views/library_menu.xml
<odoo>
    <menuitem id="menu_library" name="Library" />
</odoo>
```

#### Adding security groups, kept in /security subdirectory

Before feature can be used by regular users, access must be granted to them. In **Odoo**, this is done using security **groups**. Access privileges are granted to security groups, and users are assigned security groups. Odoo apps typically provide **two groups** for two level acccess as follows:
+ A user access level, for users performing daily operations
+ A manager access level, with full access to all features, including configurations

Security groups are organized in the same categories used for addon modules. To assign a category to a security group, find the corresponding **XML ID** for the "Services/Library" category is `base.module_category_services_library`.

```
<odoo>
    <data>
        <record id="library_group_user" model="res.groups">
            <field name="name">User</field>
            <field name="category_id" ref="base.module_category_services_library "/>
            <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
        </record>

        <record id="library_group_manager" model="res.groups">
            <field name="name">Manager</field>
            <field name="category_id" ref="base.module_category_services_library "/>
            <field name="implied_ids" eval="[(4, ref('library_group_user'))]"/>
            <field name="users" eval="[(4, ref('base.user_root')), (4, ref('base.user_admin'))]"/>
        </record>
    </data>
</odoo>


```

### [Effective Unit Testing by Eliotte Rusty Harold](https://www.youtube.com/watch?v=fr1E9aVnBxw)

The Fundamental Principle of Unit Testing = **Verify that a known, fixed input produces a known, fixed output.**

### [OCA Days 2020 - Testing best practices, tips and tricks](https://www.youtube.com/watch?v=pQ7TZELSpKY)

```
from odoo.tests.common import SavepointCase, TransactionCase, HttpCase

class TestCommonCase(SavepointCase):                                                # 1
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # disable tracking test suite wise
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))     # 2
        cls.user_model = cls.env['res.users'].with_context(no_reset_password=True)  # 3
        cls.new_user = cls.user_model_create({"name": "John", "login": "john"})

    def test_my_custom_error(self):                                                 # 5
        with self.assertRaises(exceptions.UserError) as exc:
            self.my_model.write({"a_field": "bad value!"})
        self.assertEqual(exc.exception.name, "The value is wrong sir!")


    @mute.logger(                                                                   # 7
       'odoo.models', 'odoo.models.unlink', 'odoo.addons.base.ir.ir_model'
    )

    def test_user_can_do_it(self):                                                  # 6
        vals = {...}
        rec = self.my_model.sudo(self.user_manager).create(vals.copy())
        self.assertTrue(rec)
        with self.assertRaises(exceptions.AccessError):
            self.my_model.sudo(self.user_simple).create(vals.copy())
        with self.assertRaises(exceptions.AccessError):
            rec.sudo(self.user_simple).unlink()
```

#### Base test classes
+ `odoo.tests.common.SingleTransactionCase`
+ `odoo.tests.common.TrasactionCase` - most common. Each method is run in its own transaction. The transaction cursor is not committed. setUp() test_method1() tearDown()
+ `odoo.tests.common.SavepointCase` - all methods are run in a single transaction. Each method is guarded by a savepoint (like a sub-transaction).
+ `odoo.tests.common.HttpCase` - only one you can test behavior of controller. Launches HTTP server, open any URL, run some JS in the Odoo client

##### Available on the the above test instances
+ self.registry
+ self.cr - cursor on current transaction
+ self.uid - current user id
+ self.env - current environment, **most important part**

##### Server-side form
+ A Python implementation of a form, reproduces what the client-side form does, create or edit a record just like a user would.a
```
move_form = Form(self.env['account.move'])
move_form.partner_id = partner
...
with move_form.invoice_line_ids.new() as line_form:
    line_form.product_id = product
...
invoice = move_form.save()
```

##### use `addCleanup()`
+ deallocate any resources used

##### use `unittest.mock`
```
from unittest.mock import patch

day = date(1979,5,4)
with patch.object(fields.Date, 'today', lambda *args, **kwargs: day):
    ...
    assert fields.Date.today() == day
    ...

```

##### Maximize coverage
+ Every corner case
+ Test with different users with different access rights
+ Test access errors
+ Test expected errors, shouldn't be able to deliver a product if something is not in stock

#### 1 Use `SavepointCase`
+ Suitable for the majority of our test cases, 95%
+ Use it always if no special setup is required
+ Setup records and variables only once at the setup
+ Speed

#### 2 Consider Disable tracking
+ Do it always unless you test tracking features
+ Boost tests speed

#### 3 Do not send reset password
+ Do it always unless you test reset password features
+ Avoid email sending (for real!)
+ Boost tests speed

#### 4 Avoid res.config.setting
+ res.config.settings.execute can be very heavy
+ Unless you use it to install modules (don't!)
+ Set company fields/groups/defaults/params directly
+ Fallback to res.config.settings.set_values if needed
+ Prevents strange env erros (en env reset)
+ Boost tests speed
+ Don't do in upgrade / migration sets

#### 5 Test exceptions
+ Always test the right exception and the right message
+ Make sure no same exception happens before ours

#### 6 Test permissions
+ Ensure users / groups have the right access level
+ **NEVER** use admin to test

#### 7 Disable useless logging
+ Avoid clutter in test logs
+ Speed it up

#### 8 Test onchanges and forms
+ `odoo.tests.common.Form`
+ No need to take care of collateral behaviors

#### 9 Mocking (1): Odoo helper
+ TransactionCase.patch
+ Rolls back the patch on tearDown
+ Sort of not explicit patching and not suited for other test cases
```
    def setUp(self):
        super(TransactionCase, self).setUp()
        [...]
        self.patch(type(self.env['res.partner']), '_get_gravatar_image', lambda *a: False)
```

#### 10 Mocking (2): built-in mock
+ Explicit
+ Context Manager
+ Decorator / multi patch per-test
+ Way more powerful

#### 11 Mocking(3): date/time
+ `from freezegun import freeze_time`
+ Mock date/datetime/time/any time-related value
+ Used in Odoo core since v14 (!!!)
```
    @freeze_time("2020-09-15")
    def test_eol(self):
        self.product.end_of_life_date = "2020-09-04"
        self.assertEqual(self.product.status, "endoflife")
```

#### 12 Mocking (4): request
+ `from odoo.addons.website.tools import MockRequest`
+ Mock `odoo.http.request` the right way
+ Limited override, manual hack need for setting headers and other params
```
    ctrl = InvaderControler()
    with MockRequest(self.env) as request:
        request['httprequest']['environ'] = {
            "HTTP_PARTNER_EMAIL": params["email"]
        }
        request["auth_api_key_id"] = self.backend.auth_api_key_id.id
        ctx = ctrl._get_component_context()
```

#### 13 Test Tags
+ `odoo.tests.common.tagged(*tags)`
+ odoo --test-enable --test-tags x,y,z

#### 14 Avoid HttpCase when possible
+ Slow down tests a lot, broken w/ pytest
+ Mandatory only to test route registartion
+ Split tests
+ + Test routes
+ + Test controller behavior w/ MockRequest
+ Skip it always for pytest

#### Run tests
+ Standard Odoo `$ odoo -d mydb --test-enable --stop-after-init -[i|u] my_module`
+ Pytest-odoo `$ pytest -s path/to/my_module`
+ Pytest-odoo `$ pytest -s path/to/my_module/test_feat1_`


### Step 4 - Implementing the model layer **ORM**
,w
A **`model`** describes a list of **`fields`** and can also have specific business logic attached to it. Model data structure and attached business logic are described with Python code, using an object class derived from an Odoo template class. A **model maps to a database table** and the Odoo framework takes care of all the database interactions, both in keeping the database strucre in sync with the object and in translating all transactions to teh database instructions.
+ `_name` defines the **unique ID (UID)** that will be used throughout Odoo. Uses dot(.) to seperate keyworks, most others will use underscore
+ `name` and `active` are special field names, by default Odoo framework makes special use of them. `name` is used for the record display name and `active` is used to filter outinactive records from the UI
+ **many-to-one** in database jargon, a **foreign key (FK)**. The convention is for many-to-one field names to end with *_id*
+ **many-to-many** can store links to one or more records in another model, at DB level a helper table is automatically created to store the relations between records in the two tables. The convention is to end with *_ids*

Place in `models/` directory in our module and:
```
# modules main __init__.py file
from . import models

# from models/ subdirectory __init__.py file
from . import library_book

# models/library_book.py
from odoo import fields, models

class Book(models.Model):                                   # The actual Python class name used is irrelevant for the Odoo framework
    _name = "library.book"                                  # The model ID relevant for Odoo is the _name defines the **unique ID (UID)** that will used throughout Odoo to refer to this model. Model IDs use dots (.) to sepearte keywords
    _description = "Book"

    name = fields.Char("Title", required=True)              # used for the data record title
    active = fields.Boolean ("Active?", default=True)       # used in UI to filter records
    isbn = fields.Char("ISBN")
    image = fields.Binary("Cover")
    publisher_id = fields.Many2one("res.partner", string="Publisher")
    author_ids = fields.Many2Many("res.partner", string="Author")

    # special fields Odoo automatically adds to every model
    id                  # unique numeric database ID for each record
    create_date         # record creation timestamp
    create_uid          # user who created the record
    display_name        # textual representation for the record use
    write_date          # records last modifcation timestamp
    write_uid           # who modified
    __last_update       # computed field not stored in the database used for concurreny checks



```

### Step 5 - Setting up access security

We need to grant access rights to new models before we use them, also referred to as an **access control list** or **ACL**. They indicate for a security group, what kinds of actions are allowed on records: read, write, create, and delete. Grant access on a module level but Odoo also supports row-level security, through **Record Rules** (see next section)
+ `id` is the record's external ID (aka **XML ID**), should be unique in our model
+ `name` is a descriptive title. It is informative and it is recommended for it to be **unique**
+ `model_id` is the external ID for the model we are giving access too. Automatically generated by ORM; `library.book' will generate ID `model_library_book`.
+ `group_id` identifies the security group to give permissions to. We grant access to the secuirty groups created before:
+ `perm...` fields grant acces to the `read`, `write`, `create`, `unlink` operations. **1** for `yes/true' and **2** for `no/false`


This data can be provided by a module data file, loading records into the `ir.model.access` model. The filename for CSV data files must match the model ID we are loading into.
```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_book_user,BookUser,model_library_book,library_group_user,1,1,1,0
access_book_manager,BookManager,model_library_book,library_group_manager,1,1,1,1

# don't forget to add this new file in the data key in __manifest__.py
```

#### Row-level access rules
p100 - To showcase this feature, we limit library users to not be able to see inactive books/records. *revisit*

### Step 6 - Implementing the backend view layer

Place inside a `views/` subdirectory. The **view layer describes the UI**. Views are defined using XML, which is used by the web client framework to dynamically generate data-aware HTML views.
+ **Menu items** can execute **window actions** to render **views**. The **Users** menu item processes a windown action, also called **Users**, that in turn reders a vew composition with a **list** and a **form**.
+ Several view types are available, the **three** most commonly used views are the **List/Tree**, **Form**, **Search**

Use `--dev=all` server option, which spares us from module upgrades while developing. Changes are made immediately.

#### Adding menu items
```
# views/library_menu.xml

<!-- Action to open the Book list -->
    <record id="action_library_book" model="ir.actions.act_window">         # <record> element defines a client-side window action, to open the library.book model with tree and form views enabled, in that order
        <field name="name">Library Books</field>
        <field name="res_model">library.book</field>
        <field name="view_mode">tree,form</field>
    </record>

<!-- Menu item to open the Book list -->                                    # <menuitem> for Books, running the action_library_book action, defined before 
    <menuitem id="menu_library_book"
    name="Books"
    parent="menu_library"
    action="action_library_book"
/>
```

#### Creating a form view
+ Views are data records stored in the database, in the **`ir.ui.view`** model so we need to add a datafile, with a `<record>` element describing the view.
+ The `ir.ui.view` records has a record `id` field that defines an **XML ID** that can be used for other records to reference it. The view record sets values for three fields: `name`, `model', `arch`
+ Odoo has a presentation style that mimics a paper page. This `<form>` contains two top elements: a `<header>` element, to contain action buttons, and a `<sheet>` element to contain data fields
```
# views/book_view.xml

<odoo>
    <record id="view_form_book" model="ir.ui.view">
    <record id="view_tree_book" model="ir.ui.view">
    <record id="view_search_book" model="ir.ui.view">
        <field name="name">Book Form</field>                    # Name for information purposes, it does not have to be unique, but it should allow you to easily identify which record it referes to.
        <field name="model">library.book</field>                # Model
        <field name="arch" type="xml">                          # MOST IMPORTANT FIELD is arch, as it contains the actual view definition!
            <form string="Book">
                <group>
                    <field name="name" />
                    <field name="author_ids" widget="many2many_tags" />
                    <field name="publisher_id" />
                    <field name="date_published" />
                    <field name="isbn" />
                    <field name="active" />
                    <field name="image" widget="image" />
                </group>
            </form>
        </field>
    </record>
</odoo>
```
##### Business document form views
```
<form>
    <header>
        <!-- Buttons will go here -->
        <button name="button_check_isbn" type="object" string="check ISBN" />       # name is the ID of the action that is run, (still need to add business logic)
    </header>
    <sheet>
        <!-- Content goes here: -->
        <group>
            <field name="name" />
            <field name="author_ids" widget="many2many_tags" />
            <field name="publisher_id" />
            <field name="date_published" />
            <field name="isbn" />
            <field name="active" />
            <field name="image" widget="image" />
        </group>
    </sheet>
</form>
```

### Step 7 - Implementing the business logic layer

Support the applications busines rules, such as validations and automation. Add logic.
+ `self.ensure_()` is recommended to add at the beginning of the method, to fail early if for some reason `self` is not a single record.
+ The `Model` should at least return a `True` value.

### Step 8 - Implementing the website UI

Web **controllers** are the components responsible for rendering web pages. A controller is a Pytho nmethod in a **`http.Controller`** derived class. This metho is bound to one or more URL endpoints using the `@http.route` controller. When any of these URL enpoints are accessed, the controller code executes and returns HTML to be presented to the user. The HTML rendering will usually be donw using the QWeb templating engine.
```
# views/book_list_template.xml

<odoo>
 <template id="book_list_template" name="Book List">
    <div id="wrap" class="container">
        <h1>Books</h1>
            <t t-foreach="books" t-as="book">
             <div class="row">
                <span t-field="book.name" />,
                <span t-field="book.date_published" />,
                <span t-field="book.publisher_id" />
            </div>
            </t>
        </div>
    </template>
</odoo>
```


## Section 2: Models

### Understanding the external identifer concept
An **external identifer**, also called **XML ID**, is a *human-readable string identifer* that uniquely identifies a particular record in Odoo. They are important for loading data into Odoo, allowing use to modify an existing data record or reference it in other data records.

#### How external identifers work













