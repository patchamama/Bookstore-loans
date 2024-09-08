# Welcome to [Bookstore - Loans](https://bookstore-loans-804dfdc18356.herokuapp.com/)

**Bookstore - Loans**  website is developed using Django Framework as part of Portfolio Project 4 for my Diploma in Full Stack Software Development at Code Institute.

The purpose of the application is to manage book loans: reservations, loans, extensions, and returns. It also allows commenting on books based on their availability in a bookstore, or a public or private library.

The idea is that anyone can initially reserve a book and after the reservation, the user has up to 7 days to pick up the physical book. Once the book is picked up, the administrator (bookseller) will be able to change the status of the book from reserved to loan, having a period of 30 days with the loan and it is possible to extend the loan up to 3 times (with a maximum of 3 months). To request a loan (reservation) you must be registered on the site. 
Once the book is returned, the site administrator can change the returned status and it will be available for new reservations and loans. It is also possible to cancel the reservation of a book from the book details area or the loan page.

![books-status](docs/images/books-status.png)

You can view the live site here:-  https://bookstore-loans-804dfdc18356.herokuapp.com/

## Live Site

![image](docs/images/screenshots.png)


# Table of Contents

- [Table of Contents](#table-of-contents)
  * [Repository](#repository)
  * [Agile Methodology](#agile-methodology)
  * [Features](#features)
    + [Fonts](#fonts)
    + [Existing Features and responsiveness](#existing-features-and-responsiveness)
    + [Future Features](#future-features)
- [Testing](#testing)
- [Development](#development)
  * [Basics to get up and running](#basics-to-get-up-and-running)
- [Deployment](#deployment)
- [Technologies Used](#technologies-used)
- [Credits](#credits)
- [Acknowledgments](#acknowledgments)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>



## Repository

https://github.com/patchamama/PP4-Bookstore-loans

## Agile Methodology

GitHub projects were used to manage the development process using an agile approach. 

- [Kanban board](https://github.com/users/patchamama/projects/4/views/1)

- [User stories](https://github.com/patchamama/PP4-Bookstore-loans/issues)

## Features

For the creation of the project, we took as a base the Django project start template (https://github.com/Code-Institute-Solutions/django-blog-starter-files) because of its similarity to the ideas of the site in terms of colors and structure, with some modifications.

<details>
<summary><strong>Database Structure</strong></summary>

![database-structure](docs/images/data_structure.png)
</details>

<details>
<summary><strong>Wireframes</strong></summary>

![Home-booklist](docs/images/home_booklist.png)
![bookdetails](docs/images/bookdetails.png)
![bookloans](docs/images/bookloans.png)
</details>

<details>
<summary><strong>Colors</strong></summary>

![home-screenshots](docs/images/home-screenshots.png)

The initial color palette of the chosen base templates (https://github.com/Code-Institute-Solutions/django-blog-starter-files) was maintained. 
</details>

### Fonts

I used Roboto and Lora to achieve the type of text I was looking for for this website, with a simple and classic style.

### Existing Features and responsiveness

<details>
<summary><strong>Navigation</strong></summary>

I wanted a simple and direct style to the information. The home page shows the covers and names of the books and from this information, you can access to see the details.

- Desktop

![navbar_desktop](docs/images/navbar_desktop.png)

- Mobile

![navbar_m](docs/images/navbar_m.png)
</details>

<details>
<summary><strong>Home page</strong></summary>

The navigation bar is maintained on all pages, creating unity. The book covers and title are shown with a link to directly access the book details and additional relevant information such as the number of books available for loan and the number of comments displayed. The pagination of the home page is 4 columns repeating in 3 rows allowing a maximum of 12 books to be displayed.

![home](docs/images/home-screenshots.png)

![pagination](docs/images/home_screenshots2.png)
</details>

<details>
<summary><strong>Sign Up Page</strong></summary>

This page allows the user to sign up to use the website's features by creating a username and a password. Providing an email is voluntary at this point.

- Desktop:

![signup](docs/images/singup_desktop.png)

- Mobile:

![signup-m](docs/images/signup-m.png)
</details>

<details>
<summary><strong>Sign In page</strong></summary>

This page allows registered users to log in to use the site's functions: add or delete comments and request book loans.

- Desktop:

![signin](docs/images/singin_desktop.png)

- Mobile:

![signin-m](docs/images/signin-m.png)
</details>

<details>
<summary><strong>Sign Out page</strong></summary>

This page allows the user to sign out to keep their features safe from a third party.

- Desktop:

![signout](docs/images/signout.png)

- Mobile:

![signout-m](docs/images/signout-m.png)
</details>

<details>
<summary><strong>Book details page</strong></summary>

When the user clicks on a book cover or title, this is the page where they will be directed to view the details of the book.
Only authenticated users can access the book details to borrow or comment.
Authenticated users, on the other hand, can comment - their comments will be displayed on the page upon administrator approval. There is also the possibility to delete previously approved personal comments if the user is the author of the comment.

- Desktop

What it looks like for authenticated users:
![bookdetails](docs/images/bookdetails1.png)
![bookdetails-comments](docs/images/bookdetails1-1.png)

- Mobile

![bookdetails-m](docs/images/bookdetails1-m.png)
</details>

<details>
<summary><strong>Book loans page</strong></summary>

This page is only accessible to authenticated users and allows you to view the loans requested (reservations, loans), as well as the expiration date of the loan and the possibility of requesting an extension.

- Desktop:

![bookloans](docs/images/bookloans1.png)

- Mobile:

![bookloans-m](docs/images/bookloans1-m.png)
</details>

<details>
<summary><strong>Custom Error pages</strong></summary>

I created custom error pages (400, 403, 404, 500) that are equivalent in style to the other pages of the website, so it creates a coherent vibe.

- Desktop:

![error404](docs/images/error404.png)

- Mobile:

![error404](docs/images/error404-m.png)
</details>

### Future Features

- The possibility for users to rate a book.

- If a book is not available, allow to request an email notification.

- Bookmark: ability to bookmark a book that they like.

- Email verification: make email signup mandatory and verify the user.

- Social sign-in: use Google or other forms of social sign-in features.

- Establish a maximum limit for book loans.

- The same book cannot be reserved twice at the same time.

- Add links to author and book characteristics to search for books with that author or selected characteristic.

- Validate before making a reservation if there are books available in case several simultaneous book reservations are made.


# Testing

Testing details can be found separately in the [TESTING.md](TESTING.md) file.

# Development

## Basics to get up and running

- Navigate to the [GitHub repository](https://github.com/patchamama/PP4-Bookstore-loans)
  or use [Code Institute's template](https://github.com/Code-Institute-Org/ci-full-template) to create your own workspace
- Click on Gitpod and create workspace
- Installations:

Install the server you will use when deploying to Heroku:
```sh
pip3 install 'django<4' gunicorn
```

Install supporting libraries:
- PostgreSQL & psycopg2:
```sh
pip3 install dj_database_url==0.5.0 psycopg2
```

- Cloudinary:
```sh
pip3 install dj3-cloudinary-storage
```

Create files:

- requirements.txt:
```sh
pip3 freeze --local > requirements.txt
```

- create a new Django project:
```sh
django-admin startproject bookstore .
```

- create loans app:
```sh
python3 manage.py startapp loans
```

- set up an env.py file that should look like this:
```sh
import os

os.environ['DATABASE_URL']="Your database url - see in deployment"
os.environ['SECRET_KEY']="Your secret key"
os.environ['CLOUDINARY_URL']="Your Cloudinary API environment variable - see in deployment"
```

- modify the SECRET_KEY variable in settings.py the following way:
```sh
SECRET_KEY = os.environ.get('SECRET_KEY')
```

- for deployment in Heroku, you'll need to create a Procfile

# Deployment

- This project users [ElephantSQL](https://www.elephantsql.com/) as its database solution. How you can obtain one and wire it up to your repository:
    - Use your GitHub account to sign up
    - Provide a name that ideally is consistent with your project's name
    - Select the *Tiny Turtle* (free) plan
    - You can leave the *Tags* empty
    - Select your region
    - You can access the database URL and password by clicking on your database's name

- This project uses [Cloudinary](https://cloudinary.com/) to store its media files since Heroku doesn't keep these files
    - Use your GitHub account to sign up
    - Copy your API environment variable

- This project uses [Heroku](https://heroku.com/) for deployment
    - set up an account
    - In the top right corner you'll find the button *new*
    - Click *Create new app*
    - Choose your region and a unique application name
    - Once created, navigate to *Settings*
    - Click on *Reveal Config Vars*
    - Add the keys and values from your env.py file
    - Add PORT:8000
    - Temporarily add DISABLE_COLLECTSTATIC:1 - to be removed for final deployment
    - You can choose between different methods of deployments on the *Deploy* tab
    - As well as *Manual* and *Automatic* deploys

- The deployed page is available [here](https://bookstore-loans-804dfdc18356.herokuapp.com/)

# Technologies Used

- Languages, Databases and Frameworks:

    - HTML
    - CSS
    - Javascript (Bootstrap JS)
    - Python
    - Django
    - PostgreSQL
    - psycopg2
    - Bootstrap

- Other tools:

    - [Cloudinary](https://cloudinary.com/)
    - [Font Awesome](https://fontawesome.com/)
    - [Google Fonts](https://fonts.google.com/)
    - [Balsamiq](https://balsamiq.com/)
    - [Heroku](https://www.heroku.com/)
    - [Table of contents generator](https://ecotrust-canada.github.io/markdown-toc/)

# Credits

- The [Think therefore I blog project](https://github.com/Code-Institute-Solutions/Django3blog) gave the basis of the whole project
- Tutor Support
- Slack community
- Stackoverflow
- Templates as base used: https://github.com/Code-Institute-Solutions/django-blog-starter-files
- Image to not cover: https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png
- To update the default user field in a loan with the currently logged-in user, we have used the ideas of: https://stackoverflow.com/questions/4670783/make-the-user-in-a-model-default-to-the-current-user
- To run a task at application startup (check for loans with expired deadlines and update): https://stackoverflow.com/questions/6791911/execute-code-when-django-starts-once-only
- Error 500: https://stackoverflow.com/questions/13633508/django-handler500-as-a-class-based-view 

# Acknowledgments

Many thanks to my mentor Sandeep for his support and advice. Also to the Code Institute for preparing the materials and providing a wide range of available means of learning for the students.
