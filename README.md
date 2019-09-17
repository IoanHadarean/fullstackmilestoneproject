# Wedding Planner

## User Experience Design(UXD)

### Overview

Wedding Planner is an easy to use and simple website that can help you plan the perfect wedding. The website design is clean and does not hinder accessibility in any way. Anyone can choose 
from the wide range of wedding products offered such as dresses, shoes, suits and so on and so forth. Not only does the website allow users to register and login to the website, 
but it also incorporates functionalities such as a shopping cart for purchasing products and a forum for customers to share their impressions about the website. Charts have been used as a
marketing technique to assess how many orders and sales were done in the last 3 days and the last 3 months. Furthermore, users can contact the support team (admin) in case of technical issues
They can also get the money back if they are not happy with their purchases by submitting a refund request with the reference code that they get by email when buying a product. Users can search
for products/posts and can also filter them by category/user. In addition, they can edit and add images to their profiles as well as publish and edit their own posts (posts are saved as drafts in the
first instance and they can be published afterwards). The website offers an easy to use like and comment system where customers can toggle the replies visibility. Last but not least, pagination has been 
implemented to improve navigation throughout the website. In case users forget their password, Django comes in with an easy to use reset password functionality. Wedding Planner also has a responsive implementation
due to the fact that users can access it on all types of platforms, such as mobile, tablet and desktop/PC. The main strength of the website comes from its powerful and useful checkout and payment system that allows 
users to save their shipping/billing addresses and cards for their next purchases. Another crucial factor for the business is the provision of discount coupons for new registering clients. Please check out our website at 
[https://e-commerce-web-app.herokuapp.com](https://e-commerce-web-app.herokuapp.com) and register soon as our coupons have a limited number of usages.


### Wireframes

Note: the wireframes are not entirely accurate, they only give a rough estimate on how the website will look on mobile/tablet/desktop.

#### Wireframe for desktop
<img src="/app/static/wireframes/relish-cookbook-desktop.png" alt="Relish-CookBook" border="0">

#### Wireframe for tablet
<img src="/app/static/wireframes/relish-cookbook-tablet.png" alt="Relish-CookBook" border="0">

#### Wireframe for mobile
<img src="/app/static/wireframes/relish-cookbook-mobile.png" alt="Relish-CookBook" border="0">

### Existing Features and Functionalities
The application consists of 14 HTML templates, 15 SCSS files, 17 JavaScript files, 1 utility written in JavaScript
and 6 Python files, including the env file which stores the environment variables and connection strings plus
[test_app.py](/app/tests/test_app.py), which incorporates automated tests used to measure the performance and behaviour of the project.
The main [__init__.py](/app/__init__.py) file includes a collection of all the functions and routes that have been used for
creating the logic of the website and it also stores the connections to MongoDB and MySQL. The [graphs.py](/app/models/graphs.py) file incorporates 
the functions that have been used for the creation of the statistics graphs designed with [Pygal](http://pygal.org/en/stable/), which is a Python library for designing
and creating charts. The [forms.py](/app/models/forms.py) includes the forms that have been used for registration and editing the user profiles.
Last but not least, the [values.py](/app/models/values.py) file was used for modifying the point dimensions from 
the statistics page. Finally, the [helpers.py](/app/models/helpers.py) file has been used for returning the dictionary that has been used
for filtering recipes and also includes the scripts that have been used for the statistics charts. Even though the initial plan was not to use any CSS frameworks, 
it turned out that it would take too much time to make everything from scratch. Hence the project focused more on functionalities and it reflects a steep learning curve.
Note: the [run.py](../master/run.py) has been later added for running the application and to ensure a better project structure.


#### Website Pages
1. [Register Page](/app/templates/register.html)
* Consists of a form that allows the user to create an account.
* It's constructed following a defensive design, each of the fields in the register form
will produce an inline error if the required checks are not met (For example: Passwords do not match).
* If the username or the email are already in the database, the user can not register to the website.
* When clicking register, the user is automatically redirected to the profile page, without having to go through login.
* The form fields are required, so an empty form can not be submitted.
* The form checks are achieved using a class named RegisterForm, created with the help of 
[Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) and [WTForms](https://wtforms.readthedocs.io/en/stable/).
2. [Login Page](/app/templates/login.html)
* Has a form that allows the user to login to the website.
* It's constructed following a defensive design, each of the fields in the login form
will produce an error if the required checks are not met( if the user entered the wrong password
the error will be invalid login, if the user does not exist in the database the error shown will be user not found).
* The form fields are required, so an empty form can not be submitted.
* When clicking login, the user is automatically redirected to the profile page.
3. [Profile Page](/app/templates/profile.html)
* Allows the logged in user to update his/her profile.
* The update profile form is constructed following a defensive design, each of the fields 
in the login form will produce an error if the required checks are not met, except the about me field
(For example: if the user does not choose a png, jpeg or jpg file, an error is rendered below the input file field).
* The form checks are achieved using a class named EditForm, created with the help of 
[Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) and [WTForms](https://wtforms.readthedocs.io/en/stable/).
* The local date is shown on each user's profile.
* When clicking the update button, the user's profile is automatically updated, provided there are no errors.
* When clicking the cancel button, a modal opens asking the user for confirmation (if the user clicks reset progress
the form is resetted, if the user clicks continue he/she can proceed to updating his/her profile).
* The recipe cards for each user are shown on the profile page.
* If the user clicks on the edit recipe button she/he will be redirected to the edit page for that specific recipe.
* Whenever a user clicks on the delete button, a modal pops up asking the user for confirmation(if the user clicks delete
the recipe is deleted from the database and his/her profile, if the user clicks cancel the delete modal closes).
* If the user clicks on the recipe image or the view recipe button, she/he will be redirected to the view
for that specific recipe.
4. [Recipes Page](/app/templates/recipes.html)
* It has a form with three selects, that allow the user to filter recipes by a combination of three: 
allergens, cuisines and courses.
* The filter results are shown on active input, the recipe container is cleared when the select options change.
* When clicking the filter recipes button, the corresponding recipes are shown according to the filters,
as well as the number of results. 
* Users can go back to all recipes at any time by clicking the all recipes button.
* Users can navigate through the recipes with the help of pagination, which is implemented
both for all recipes and the filtered recipes (6 recipes per pagination page).
* The filter button is disabled, unless the user clicks on a filter.
* The header welcome message changes every time the user accesses or refreshes the page.
* If a user clicks on the image of the recipe or the view recipe button, he/she is redirected to the
view for that specific recipe.
* All users can view the recipes page and filter through recipes, regardless if they are logged in or not.
5. [Search Page](/app/templates/search_recipes.html)
* It has an input that allows users to search recipes when clicking on the search button.
* The number of results are shown on active input, as well as after clicking the search button.
* All users can view the search page and search recipes, logged in or not.
* The search button is disabled if the input is empty or if the input has less than three characters.
The input is also trimmed of white spaces.
* The recipe container is cleared on input change.
* Users can go back to all recipes at any time by clicking the all recipes button.
* Pagination is implemented for the search recipes results (6 recipes per pagination page).
* If a user clicks on the image of the recipe or the view recipe button, he/she is redirected to the
view for that specific recipe.
6. [Statistics Page](/app/templates/statistics.html)
* Has three graphs that have been constructed with the help of functions existent in the 
[models.py](/app/helpers.py) Python file.
* The first graph (dot chart) shows the recipe statistics ingredients per cuisine. That is explained by how
many recipes from a specific cuisine contain egg, milk, sugar, flour, salt, water, garlic, vanilla or butter
(For example: 2 out of 4 French recipes contain egg).
* The second graph (solid gauge chart) illustrates the recipes allergens statistics in % (For example: the garlic
allergen is found in 41.66% of the recipes).
* The third graph (gauge chart) displays the average calories by cuisine (For example: the Greek cuisine has an average
of 599 calories).
* Logged in or not, all users can look at the statistics page.
7. [Database Recipe Page](/app/templates/get_recipe.html)
* When a user who is not logged in clicks on the like/dislike or rate recipe button, a modal pops up which requires the user
to login if he/she has an account or to register if he/she does not have an account.
* The user is redirected back to the recipe he was viewing after registering/logging in to the website.
* The user can view all the details of the recipe and he can also click on the add recipe button to add her/his own recipes.
* A logged in user can like and dislike a recipe the following way: when she/he clicks on the like button, the number of likes
goes up by 1 and dislikes go down by 1 if they are not 0, when he/she clicks on the dislike button the number of dislikes goes up by 1
and the number of likes goes down by 1 if the number is not 0 (Note: the page does not refresh on like/dislike due to AJAX).
* When a logged in user tries to click on the rate button, a modal pops up that allows the user to fill the number of stars 
according to his/her rating. Upon clicking on save and continue, the rating is saved and the average rating for that recipe is 
updated.
* When a logged in user tries to rate a recipe, the initial rate text is set to `Rate Recipe`, but if the user tries to update
his previous rating, the rate text changes to `Edit Rating` (Note: this happens for every recipe a logged in user tries to rate).
8. [User Recipe Page](/app/templates/get_user_recipe.html)
* The user can view all the details of his/her recipe and he can also click on the add recipe button to add another recipe.
* If the user clicks on the edit recipe button she/he will be redirected to the edit page for her/his specific recipe.
* Whenever a user clicks on the delete button, a modal pops up asking the user for confirmation (if the user clicks delete
the recipe is deleted from the database and his/her profile and he/she is redirected to the profile page, if the user clicks cancel 
the delete modal closes).
9. [Add Recipe Page](/app/templates/add_recipe.html)
* It has a form that allows a user to fill the recipe name, add ingredients and instructions, as well as choose the cuisine,
course and allergen for the recipe that they are trying to add.
* The user can add instructions and ingredients by clicking on the add icon and can delete ingredients and instructions
by clicking on the clear icon.
* The user has the ingredient and instruction fields preserved through sessionStorage. (Note: this feature needs to be 
modified by allowing the user to save his progress, so the form values are saved as well).
* Whenever a user clicks on the reset progress button, a modal pops up asking for confirmation (if the user clicks on the reset
progress button, the form is cleared, if the user clicks on the continue button, she/he can proceed to add her/his recipe).
* A recipe needs to have at least one instruction and at least one ingredient, so when a user clicks on the first ingredient or 
the first instruction an alert is shown at the top of the page.
* It's constructed following a defensive design, each of the fields in the add recipe form will produce an error if the required 
checks are not met (the recipe name needs to have at least 6 characters, an ingredient must have at least 3 characters, an
instruction must have at least 4 characters, all the form fields are required).
* When the user clicks on the add recipe button, the recipe is added in the user recipes collection and the user is redirected to
his/her profile, where he/she can see the recipe.
10. [Edit Recipe Page](/app/templates/edit_recipe.html)
* It's constructed following a defensive design, each of the fields in the edit recipe form will produce an error if the required 
checks are not met(the recipe name needs to have at least 6 characters, an ingredient must have at least 3 characters, an
instruction must have at least 4 characters, all the form fields are required).
* A recipe needs to have at least one instruction and at least one ingredient, so when a user clicks on the first ingredient or 
the first instruction an alert is shown at the top of the page.
* When a user clicks on the cancel button, he/she is redirected to the view for that recipe (The redirect could have been to the
previous page, but this allows the user to find out that his/her modifications were recorded to the database).
* The user has the ingredient and instruction fields preserved through sessionStorage. (Note: for the edit recipe form, the inputs
are not preserved when he/she leaves the edit page. An extra feature could be added so each user could save his/her edit progress).
11. [Error 404 Page](/app/templates/error404.html)
* Comprises a custom page not found error.
12. [Error 405 Page](/app/templates/error405.html)
* Comprises a custom method not allowed error.
13. [Error 500 Page](/app/templates/error500.html)
* Comprises a custom server error.
14. [Base Template](/app/templates/base.html)
* Includes all the scripts and css files that have been used for the construction of the other templates.
(Note: 6 additional helper templates have been used for creating the cancel and delete modals, navbar, as well as
inline errors and alerts. They can be found [here](/app/templates/includes)).
15. Additional Notes
* When clicking logout, the user is automatically removed from the session.
* Added longer set timeout for alerts for improved user experience.
* Paranoid was added to automatically log out the user on a different device. (See notes in 
[app.py](../master/app/__init__.py))
* Added SSL certificates and Flask-SSLify that turned out to be no longer needed, but the packages
and imports were kept in case of further uses.
* Added timeout after an hour for a logged in user.

### User Stories
* A user can register to the website with an username, email and password.
* A user can login to the website.
* A user can logout from the website.
* A user can request a password reset.
* A user can choose a new password for his/her account.
* A user can edit his/her username and email and add a picture to his/her profile.
* A user can access the contact us page and send an enquiry using the contact form.
* A user can access the refund page and send a refund request.
* A user can access the charts for viewing orders and sales in the last 3 months and last 3 days.
* A user can search for posts, view posts and navigate through them using the pagination.
* A user can access posts directly from the search typeahead.
* A user can add a post (saved in drafts first) and go back to all posts.
* A user can access his/her own drafts.
* A user can publish a post and add a comment to a post (comments have to be approved
* by the admin first).
* A user can reply to other people's comments.
* A user can view/hide replies for a comment.
* A user can edit and delete his own posts and comments/replies.
* A user can like/dislike other peoples' posts.
* A user can view the title, text and published date of a post.
* A user can view all the products on the home page and navigate through them.
* A user can search products and filter them by category.
* A user can access products directly from the typeahead.
* A user can view the details of a product and access products with the same category
* from the details view.
* A user can add/remove a product from cart.
* A user can update a product quantity in the cart.
* A user can view the details of an order in the order summary and continue shopping.
* A user can navigate to the checkout page from the order summary and go back to order summary
* from checkout.
* A user can add a discount coupon for an order.
* A user can not use a discount coupon more than once.
* A user can not use a discount coupon for orders with the amount less of equal to the value
* of the coupon.
* A user can add a shipping/billing address for an order and save it as default/update it.
* A user can use a default shipping/billing address if there is one.
* A user can navigate to the payment page and back to checkout from the payment page.
* A user can pay using a new card or with the default card if there is one.
* A user can save a card for future purchases.
* A user can set the new default card for future purchases.
* A user can remove a card from the saved cards and update the card details.
* Besides the in-built Django admin features, an admin can approve/disapprove a user's comment,
set the refund status as `accepted` and the order status as `being delivered` or `received`.


### Features Left To Implement

1. A thing can be added to the website is a functionality for saving progress when the user tries to add a recipe.
2. Another functionality that can be implemented is to allow the admin to approve user recipes in order to add them
to the database recipes.
3. Website design can be improved and CSS fixes can also be made.
4. Pages on screen resizing should look much better, but since the project focused more on functionalities, this aspect was
neglected. 
5. The Python code could be better structured with the help of classes.
6. A comments section (that also contains likes and dislikes) can be added to each recipe so users can post their opinions.
7. A chat could be added so that users could interact with each other.
8. A remember me functionality can be added for login, as well as reset password.



## Bugs Fixed

* Fixed footer span alignment issues.
* Needed to import create_logger from flask.loggings since app.logger.info was not working and the inline
errors would not display for the form helpers.
* Fixed welcome message and styled login and logout buttons flickering bug by adding a hidden class 
to html and then removing it on load. This was an issue related to the fact that the HTML needed to be hidden
before the random message would actually show up on the page.
* Fixed bug with pagination (pagination buttons added even if the number of results exceeded the total number
of recipes) by checking if the offset + limit is less than the total number of recipes.
* Added fix for footer positioning (in the middle of the page) when searching and filtering recipes by adding a custom
`vh100` class for the footer, setting the min-height to `100vh`.
* Fixed overflow for recipe section.
* Implemented fix for bug with likes/dislikes by adding liked and unliked flags for each recipe, so that users could not like 
or dislike a recipe more than once.
* Fixed bug with edit rating text, which actually needed to be inserted into the database before the user would
click on the rate button.
* Added fix for view recipe bug when the user was not in session.
* Fixed image path bug on profile (caused by `urandom` module) by replacing "/" from the random string with "|".
* Implemented fix for bug with rate text changing for each user after one user already rated a specific recipe.
* Fixed bug for pagination when filtering and searching recipes. This was accomplished with some checks in the
[recipes](/app/templates/recipes.html)  and [search_recipes](/app/templates/search_recipes.html) and by revising the 
pagination logic in the filter and search routes.
* Fixed bug with local time not being shown, converted date from `datetime.utcnow()` to local string using JavaScript.
* Implemented fix for broken image links by adding a custom image on error for the recipe images and profile image.
* Fixed bug with clear and add icons when removing an ingredient or instruction. Needed to find the parent of the
button when the button was clicked and the parent.parent of the icon when the icon was clicked.
* Added fix for global MySQL cursor not being closed in the profile route.
* Added fix for search results on active filtering by performing debouncing for the AJAX requests. Also aborted the null requests.
* Fixed flash of original content (FOOC) when trying to remove the first ingredient and instruction from the add and edit
recipe forms by disabling the remove button. It is to be agreed that the fix could have been better since the alerts timeout is 
slightly too fast. jQuery could have been used to prevent it, but only vanilla JS was used for the project.
* Fixed delete recipe bug caused by the ID of the recipe.
* Fixed security flaws caused by accessing user specific urls even if the user is not logged in.
* Fixed rating bug caused by not initialising the rating of a recipe to 0.
* Fixed bug with cancel update modal not firing up.
* Fixed average rating bug caused by the instance count of ratings for a certain recipe that also included `0`.
* Fixed bug with likes (dislikes would not go down by 1 after liking a recipe and likes would not go up by 1 after disliking
a recipe). The approach was to use two separate spans for likes and dislikes and to toggle the number of likes and dislikes.
The only condition was for likes and dislikes to be greater than or equal to 0.
* Fixed localStorage bug not being cleared by adding sessionStorage (this was also fixed with the JavaScript utility,
but it turned out that sessionStorage is a much better solution, at least for the scope of this project; it is to be 
mentioned that for the next improvements on the website, localStorage will be used, hence why the utility was not deleted).\
Note for the persons that will look at the website in more depth or the assessors of the project:
There is a bug/inconsistency in the website that I am totally aware of. When adding new inputs and deleting
them, an extra input is added on page refresh, even if the first input (the one persisted through HTML) was deleted. 
For solving this inconsistency/bug, the approach is to just use one input for adding recipes, and then append the 
deletion icon to each added input.
Additional Note: even if the creator of the website is going to get marked down for this aspect, he believes it was 
worth mentioning, and since he tries to be critical about himself, it was the right choice to make.


## Tech Used

### Front-End Technologies

1. **HTML5**, **CSS3** and **JavaScript**
    <br>**HTML5** was used  to construct the templates used in the project. **CSS3** was used to improve the
    design and the appearance of the website. **JavaScript** was used for creating the AJAX for likes, the products
    and posts search, the payment script, reply toggle, `Back` functionality, checkout checkboxes toggle, `active` class
    for home product navbar items.
2. **Bootstrap v4.0.0**(https://getbootstrap.com/docs/4.0/getting-started/introduction/)
    <br>**Bootstrap** was used to give the project a responsive layout.
3. **MDBootstrap**(https://mdbootstrap.com)
    <br>**MDBootstrap**, same as **Bootstrap** was used to build the responsiveness of the website.
    Note: Both **MDBoostrap** and **Bootstrap** use **jQuery**(https://jquery.com).
4. **Font Awesome v5.8.2**(https://use.fontawesome.com/releases/v5.8.2/css/all.css)
    <br>Font and icon toolkits based on **CSS** and **LESS** that were used to style the website.
5. **Chart.js**(https://www.chartjs.org)
    <br>**Chart.js** was used for constructing the charts statistics (orders and sales).


### Back-end Technologies
1. **Python**(https://www.python.org)
   <br>**Python** is a powerful programming language that is used to build websites in a 
   relatively short amount of time.
2. **Django**(https://www.djangoproject.com)
   <br>**Django** Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.
3. All packages used in this project can be seen in the [requirements.txt](../master/requirements.txt) file.


## Testing

1. Code was written and tested using Cloud9 and Cloud9 debugger tools.
2. All HTML and CSS code used on the site has been tested using [The W3 CSS Validation Service](https://jigsaw.w3.org/css-validator/) 
and [The W3 Markup Validation Service](https://validator.w3.org/). There were no CSS errors, there were 6 CSS warnings related to font-smoothing and transition 
unknown vendor extensions. There were 3 HTML errors and one warning found, a duplicated id `stripeBtn` due to payment form toggle and the value of the for attribute
of the label element must be the ID of a non-hidden form control for the `private-stripe-element`.
3. All Javascript code on the website has been tested using [JSHint](https://jshint.com/). There were no errors and 67 warnings found related to let 
available in ES6 and Mozilla JS extensions and Functions declared within loops referencing an outer scoped variable may lead to confusing semantics.
4. A lot of manual testing has been done for this project to ensure the website looks well on all devices and to ensure that the functionalities of the project are working
correctly. Therefore, site was viewed and tested in the following browsers:
<br>    i Google Chrome
<br>    ii Mozilla Firefox
<br>    iii Opera
<br>    iv Microsoft Edge\
The website has limited support for Internet Explorer and Safari.
5. Added automated unit tests for models, views, forms and apps for each Django-app and used the `coverage` Python module to assess
the testing coverage of each app. The `coverage` module was installed by typing `pip install coverage` in the terminal.
Each Django app was tested individually using the command  `coverage run --source=app-name manage.py test app-name` and the report was
done with the command `coverage report`. In order to get the HTML templates with the results the following command was issued: `coverage html`.
There are `141` written automated tests for the entire project, `17` for the `accounts` app, `5` for the `contact` app, `9` for the `charts` app,
`33` for the `forum` app, `17` for the `search` app and `60` for the `shoppingcart` app. (See below the coverage report for each app)

    <img src="/ecommerce/static/img/coverage_report_accounts.png" alt="coverage-report-shoppingcart" border="0">
    
    <img src="/ecommerce/static/img/coverage_report_contact.png" alt="coverage-report-contact" border="0">
    
    <img src="/ecommerce/static/img/coverage_report_charts.png" alt="coverage-report-charts" border="0">
    
    <img src="/ecommerce/static/img/coverage_report_forum.png" alt="coverage-report-forum" border="0">
    
    <img src="/ecommerce/static/img/coverage_report_search.png" alt="coverage-report-search" border="0">
    
    <img src="/ecommerce/static/img/coverage_report_shoppingcart.png" alt="coverage-report-shoppingcart" border="0">

6. Tested the Python code for [PEP8](https://pypi.org/project/pep8/) standards and solved numerous issues regarding
beautifying the code. There were a number of errors related to the length of the lines that were ignored because they 
would decrease readability of the code, not increase it.


## Deployment
Note: the coding for the project was done in Cloud9. 
1. Created a new git repository by typing *`git init`* in the terminal.
2. Added the git remote by typing *`git remote add origin https://github.com/IoanHadarean/fullstackmilestoneproject.git`* in the CLI.
3. Created a virtual environment (venv). Note: If the editor you are working on does not have a virtual environment already set up,
you would need to create one yourself. Please refer to this documentation for creating a venv 
([Virtual Environment and Packages](https://docs.python.org/3/tutorial/venv.html)). 
4. Created the `requirements.txt` file using *`pip freeze > requirements.txt`*. This file was necessary for the deployment process
since it allowed Heroku to figure out what packages should be installed when deploying the app on the production server.
4. Created a Procfile that declared the type of application, in this case a web application. The command used for initialising the Procfile
was *`web: gunicorn ecommerce.wsgi:application --log-file - --log-level debug`*. The `--logfile` and `--log-level debug` were used for
more detailed information on debugging.
5. Added a repository to deploy from in the `Deploy` section on [Heroku](https://www.heroku.com) and `Enabled automatic deploys`
from that branch.
Note: Heroku is a cloud-based platform that makes it easy to deploy and scale Python apps, regardless if the framework used is
Flask or Django.
7. Added the config variables to Heroku in the `Settings` section:


|            Key            |                  Value            |
| ------------------------  |:-------------------------------:  |
|  *`SECRET_KEY`*           |   *`SECRET_KEY_STRING`*           |
|  *`DATABASE_URL`*         |   *`DATABASE_URL_STRING`*         |
|  *`SENGRID_API_KEY`*      |   *`SENGRID_API_KEY_STRING`*      |
|  *`STRIPE_SECRET_KEY`*    |   *`STRIPE_SECRET_KEY_STRING`*    |
|  *`AWS_ACCESS_KEY_ID`*    |   *`AWS_ACCESS_KEY_ID_STRING`*    |
|  *`AWS_SECRET_ACCESS_KEY`*|   *`AWS_SECRET_ACCESS_KEY_STRING`*|
|  *`DISABLE_COLLECTSTATIC`*|   *`1`*                           |


### Getting the code up and running
The project runs on a production server called Heroku. If you want to run the project locally please follow these instructions:
1. Download and install Python3 via the Command Line Interface(CLI) (Make sure you are using Python3, the project won't run on Python2). 
In order to check the version of Python installed type python --version in the terminal.
2. Clone the following project using *`git clone https://github.com/IoanHadarean/fullstackmilestoneproject.git`* or download it and then unzip it
3. Install the packages needed for the project via the terminal by typing (sudo) pip3 install -r requirements.txt.
4. Add all environment variables to an env.py file that is in the following format:

    All connection details must be in a string format.\
    Note: you can run the project with the development settings as well, but for accessing the
    full functionalities of the app you would need to create a STRIPE, SENDGRID and AWS (S3) account in
    order to get the keys necessary for sending emails, making payments and storing media and static files.
    For additional information on how to setup these accounts please take a look at the documentation on the
    following websites: [Stripe](https://stripe.com), [Sendgrid](https://sendgrid.com) and [AWS](https://aws.amazon.com).
    ***
    ```import os
    os.environ.setdefault("SECRET_KEY", SECRET_KEY_STRING)
    os.environ.setdefault("DATABASE_URL", DATABASE_URL_STRING)
    os.environ.setdefault("SENGRID_API_KEY", SENGRID_API_KEY_STRING)
    os.environ.setdefault("STRIPE_SECRET_KEY", STRIPE_SECRET_KEY_STRING)
    os.environ.setdefault("AWS_ACCESS_KEY_ID", AWS_ACCESS_KEY_ID_STRING)
    os.environ.setdefault("AWS_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY_STRING)
    ```
    ***
    Additional Notes: you don't need to import the env file as it is already imported in the project\
5. Run the app by typing *`python3 manage.py runserver $IP:$PORT`* in the terminal. Alternatively, you
could set up a shortcut for running the app by adding an alias into the *`~/.bashrc`* or *`/etc/bash.bashrc`*
file like so *`alias python3 manage.py runserver $IP:$PORT="run"`*.
Note: the debug is by default set to FALSE, but you can set it to TRUE to allow debugging.


## Credits

I would like to thank all the people who gave constructive feedback on the website and took their time to test it,
including my mentor Moosa Hassan.

### Media and Information

The `images` and `information` used on this site were obtained from:
1. [WED2B](https://www.wed2b.co.uk)
2. [BrilliantEarth](https://www.brilliantearth.com)
3. [MyTheresa](https://www.mytheresa.com)
4. [Moss](https://www.moss.co.uk)
5. [Bloominous](https://bloominous.com)
6. [Nordstrom](https://shop.nordstrom.com)

The `domains` used for whitelisting in [Sendgrid](https://sendgrid.com) were obtained from
[AWeber](https://blog.aweber.com/email-deliverability/top-10-email-domains-of-2006.htm).

