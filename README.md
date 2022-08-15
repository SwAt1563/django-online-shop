## The Requirements

1. ### The User Requirements

   - Build a `catalog page`
   - Create a `shopping cart`
        - Create `context processor` for the cart
   - Create customer `orders model`
   - Lunching asynchronous task with `Celery`
   - Integrating a `payment gateway` by using Braintree sandbox account
   - Export orders to `CSV` files
   - Generate `PDF` file for each order, and send it to the customer email
   - Create a `coupon` system
   - Add `internationalization` system, by support english and spanish languages on the site
        - `Change the urls` depend on the current language
        - Change the `content text` depend on the current language
        - `Translating templates` by using tags
        - Allow users to `change between languages`
        - Use `Rosetta` for translation interface
        - Translating models with `django-parler`
   - Add `localiztion` system
        - `Format the dates` on the page depend on the user country
   - Use `django-localflavor` for make limitations on the form fields inputs depend on the country
   - Building a `recommendation engine`
        - Run `redis-server` for save the recommendations in the cache 
     
2. ### System Requirements
   
   - Clone the repository 
   - Docker steps:
        - Go to `docker-compose.yml` level on command line
        - RUN this command `docker-compose build`
        - RUN this command `docker-compose up -d`
        - Now you can visit the shop site on this [link](http://localhost:8000/)
        - You can access the administration site on this [link](http://localhost:8000/admin)
            - Initial account: `username=admin`, `password=1`
   - Python Virtual Environment on Windows steps:
     - Create python virtual environments on the same level of manage.py file
          ```
          python -m venv venv
          ```
     - Create the requirements.txt file on the same level of manage.py file if not exist
        
     - Run this command in the terminal of virtual environment
          ```
          pip install -r requirements.txt
          ```
     - For Windows OS, you should download [GTK3](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases) 
     `Install DLL files to lib` , then change the path of the GTK3 in `myshop\orders\views.py` file
     - You should run redis-server before run the project, if you on Windows OS
       [download](https://riptutorial.com/redis/example/29962/installing-and-running-redis-server-on-windows) it
   
     - You can use this command in the terminal of virtual environment for create user on your administration page
          ```
          python manage.py createsuperuser
          ```
     - Run this command in the terminal of virtual environment for open the server connection on localhost
          ```
          python manage.py runserver
          ```
     - Now you can visit the [administration page](http://localhost:8000/admin) and
     the [shop page](http://localhost:8000/)