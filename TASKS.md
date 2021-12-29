# Steelkiwi Python Test Task


### Start project
* `git clone https://repo.url` - clone repo
* `virtualenv venv --python=/path/to/python` - configure virtual environment
* `pip install -r requirements.txt` - install requirements
* `createdb test_products_task` - create PostgreSQL database
* `cp env.example .env` - crate you env file with settings
* `python manage.py migrate` - migrate database
* `python manage.py runserver` - run development server


#### Parts of implemented tasks:
##### Basic level task
* Made and set up a new project for Django 4
* Updated the slug field of the Product model to unique
* Added the image field of the Product model
* Added all models to the admin interface
* Finish provided unit tests.
* Implemented a page that shows a list of all categories with a
number of products in each. Where the list items must be links to
the corresponding category page
* Implemented a page that would show a list of all products in
the given category with pagination. Display the following
for each product:
● title ● price ● small thumbnail ● number of likes 
with using the category slug in the URL
* Added the ability to “like” products. Would be saved either the account of
the person who has liked something or their IP address (for
unauthorized users). Allow only one like per user/IP.
* Added the ability to comment products on their respective
pages and display all recent comments. Comment length limited to 500 symbols.
Authorization should not be required

##### Advanced level task
* Added WSYWIG editor(django_ckeditor) with allow to upload images to Product description.
* Added on the main page, display the list of top 10 most popular
products (by the number of likes)
* Added track of all page loads with date, slug, and user or ip if unauth fields.
* Implemented a management command that generates a
CSV file with products. Columns should be the following: ‘ID’ ‘Title’
‘Number of Comments’ ‘Number of Likes’
* Implemented display a list of products in the sidebar - one
from each category on each page. “NEW ARRIVALS” on frames. Made with single sql request.
* Included the ability to add products to the shopping cart.
* Added the ability to create orders and pay for the products in
the cart through Stripe.
* Added product grade field to product model with such
choices:‘base’ ‘standard’ ‘premium’
Added data migration to set all products into the ‘standard’
class(grade).
*  On the category page, add a price filter to the product list.
It should take two inputs, with minimum and maximum
prices being set by default. It’s okay to reload the page on
submit.

##### Advanced level task that wasn't implemented
* Add a page with a list of all orders made by the user.
* Add parameters to create csv file that would allow setting: file destination
whether to export products without likes whether to export products without comments
* Add statistics by the number of page loads per day for the
last week on the main page.
* Add filters for the number of likes and comments (e.g.
“show products with at least one like/comment”).
* Implement a page that will show a list of products by filter
from the previous point.
* On the main page, inside of the ‘Choice of week’ section,
display the number of ‘base’ products (>10 likes), ‘standard’
products (>5 likes) and the total number of ‘premium’
products. In order to accomplish this task, please
implement it with a single query to the database.
