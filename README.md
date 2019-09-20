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
users to save their shipping/billing addresses and cards for their next purchases. Another crucial factor for the business is the provision of discount coupons for new registering clients. Please check out the 
website at [https://e-commerce-web-app.herokuapp.com](https://e-commerce-web-app.herokuapp.com) and register soon as coupons have a limited number of usages.


### Wireframes

Note: the wireframes are not entirely accurate, they only give a rough estimate on how the website will look on mobile/tablet/desktop.

#### Wireframe for desktop
<img src="/ecommerce/static/wireframes/home-page-desktop.png" alt="home-page-desktop" border="0">

#### Wireframe for tablet
<img src="/ecommerce/static/wireframes/home-page-tablet.png" alt="home-page-tablet" border="0">

#### Wireframe for mobile
<img src="/ecommerce/static/wireframes/home-page-mobile.png" alt="home-page-mobile" border="0">

### Existing Features and Functionalities
The application consists of 6 Django apps that were created using the command `django-admin startapp app_name`:
`accounts`, `contact`,  `charts`, `forum`, `search`, `shoppingcart`. All the static and media files used in the app
were collected on [AWS S3](https://aws.amazon.com/s3/) using the command `python3 manage.py collectstatic`. All the emails
are sent using [Sendgrid](https://sendgrid.com) and the product payments are done using [Stripe](https://stripe.com).


#### Django Apps
1. [Accounts App](/accounts)
2. [Contact App](/contact)
3. [Charts App](/charts)
4. [Forum App](/forum)
5. [Search App](/searc)
6. [Shoppingcart App](/shoppingcart)


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

1. A subscribe to our email newsletter functionality.
2. Another functionality that can be implemented is for the admin to approve/disapprove posts.
3. The shopping cart app could be split into several more apps.
4. A subscription type could be implemented for registered users.
5. The search for posts and products could be slightly improved.


## Bugs Fixed

* Fixed bug with registration route misspelling.
* Fixed bug with footer aligned in the middle of the page and posts CSS positioning.
* Fixed bug with profile not being automatically created when the user was registered
with a try/except block when the user profile did not exist.
* Fixed bug with media path not being correctly configured.
* Fixed bug with drafts not being shown for a user and added login required so the route
could not be accessed when the user would be logged out.
* Fixed bug with item quantity going below 0 in the shopping cart.
* Fixed bug with coupon typo that prevented the coupon from being added to an order.
* Fixed bug with total item price not being correctly calculated with the discount coupon.
* Fixed bug with cart item count in case there are no items and bug with item quantity when adding the same
item to the cart.
* Fixed bug with all authors being shown on the dropdown by overwriting the `__init__` function for the `PostForm`
class. (Note: In later releases, the author was no longer shown)
* Fixed bug with pagination not being shown for searching posts and products.
* Fixed bug with charts info not being shown if there were no orders/sales.
* Fixed default image for profile by providing a static image for the user profile 
if there were no saved images.
* Fixed bug with active class not being changed throughout the navbar products category filter.
* Fixed bug with default shipping address/billing address not being overwritten if there already was a default one
and the user wanted to set a new shipping/billing address as default.
* Fixed saved payment cards so each user could not store more than 3 payment cards.
* Fixed loader/spinner for charts and the speed of getting the charts data by optimizing the for loops used.
* Fixed width/height for default user profile image.
* Fixed bug with coupon that could be added multiple times for the same order.
* Fixed bug with typeahead search results being shown even if there was no search word by debouncing it.
* Fixed overflow for pagination on mobile and search typeahead overflow.
* Fixed bug with search for products and posts (users could only get results for typing a sentence separated
by spaces with words of length 1 (`a b e f`) or length more than 1(`du tr dress`), but not the combination of the
two (`a tr ring`).


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
done with the command `coverage report`. In order to get the HTML templates (auto generated folder `htmlcov`) with the results the following 
command was issued: `coverage html`.
Note: needed to change all the API and secret keys in the env file and add `htmlcov` to gitignore since htmlcov actually stored an
HTML template for the env file as well.
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
including my mentor Moosa Hassan. Special thanks goes to [JustDjango](https://www.youtube.com/channel/UCRM1gWNTDx0SHIqUJygD-kQ?&ab_channel=JustDjango)
for the Youtube tutorials that I used for some of the features in the `shoppingcart` app and to [Corey Schafer](https://www.youtube.com/user/schafer5)
for the Youtube tutorials that I used for `pagination` and `user profile`.

### Media and Information

The `images` and `information` used on this site were obtained from:
1. [WED2B](https://www.wed2b.co.uk)
2. [BrilliantEarth](https://www.brilliantearth.com)
3. [MyTheresa](https://www.mytheresa.com)
4. [Moss](https://www.moss.co.uk)
5. [Bloominous](https://bloominous.com)
6. [Nordstrom](https://shop.nordstrom.com)

The `ecommerce` Bootstrap template used for the `shoppingcart` app was obtained from [MD-Bootstrap](https://mdbootstrap.com/freebies/jquery/e-commerce/).

The `domains` used for whitelisting in [Sendgrid](https://sendgrid.com) were obtained from
[AWeber](https://blog.aweber.com/email-deliverability/top-10-email-domains-of-2006.htm).

License Agreement: This project is for educational purposes only no content is intended for public use.