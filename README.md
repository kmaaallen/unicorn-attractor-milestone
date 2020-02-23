# Unicorn Attractor
Unicorn Attractor is a site designed to allow users of the fictional 'Unicorn Attractor' software to log issues and request new features. On the issues and feature overview pages users can see the progress of the ticket as either reported/requested, in progress or completed. Users can also see how many votes a ticket has, its priority level and any comments added to the ticket depending on their level of access.

In order to be able to request new features users subscribe to a monthly payment which allows them full access to the features module. At any time, subscribed users can unsubscribe or update their card details.

Non-subscribed users with an account are able to view the features requested but can neither upvote, comment nor request new ones. The intention behind being able to view these was to give users an idea of what kind of access they could have if they subscribed to the service. Once subscribed, users are able to request new features which will improve the software and allow users to better use the software in their business.

The site owner is able to use the money from these subscriptions to fund development on these new requests as well as bug fixes. They pledge to spend 50% of their working hours working on the new requests and the remainder goes on bug fixes.

The site can be viewed [here](https://unicorn-attractor-milestone.herokuapp.com/).

This project is a full-stack frameworks milestone project for code institute.
Built using the GITPOD template provided by Code Institute.

## UX
### Goals
The goal of this site is to allow users of the fictonal 'Unicorn attractor' software to report issues and request new features.
The owners of the software use this information to improve their tool and provide new features. Allowing new feature requests only
by subscription funds the developers, allowing them to continue to expand the tool.

The site provides this information in a single place and the developers (as admins) can view, update and move tickets as they work on them.

### User Stories
I used the below user stories to help plan my features:

- As a unicorn attractor user I want to be able to report an issue
- As a unicorn attractor user I want to be able to request new features
- As a unicorn attractor user I want to be able to contact the owners of the software
- As a unicorn attractor user I want to be able to move reported issues up the queue by upvoting
- As a unicorn attractor user I want to see all reported issues and relevant information about the tickets
- As a unicorn attractor user I want to be able to comment on tickets to add more information
- As a unicorn attractor user I want to be able to manage my account to that I can reset my password if I forget, cancel my subscription or update my card details
- As a unicron attractor user I want to view my specific issues and tickets


- As a unicorn attractor developer I want to be able to see tickets from end users
- As a unicorn attractor developer I want to be able to collect payment to fund work to fix issues and develop new requests
- As a unicorn attractor developer I want to be able to update all tickets, move them to the appropriate queue and add additional information
- As a unicorn attractor developer I want to be able to collect subscription payments securely and have a view of my subscribers
- As a unicorn attractor developer I want to restrict access to the features module based on subscription level.
- As a unicorn attractor developer I want to recieve messages from users via a contact form so I can act on them if necessary


I also created some basic wireframes, which I used as the starting point for my designs.
 
I wanted to use a kanban style board to display tickets as I find this visually appealing and it seems logical to have this as a quick view of where tickets are sitting.
I wanted to keep the design relatively simple and with high contrast colours.

## Layout
I wanted to keep the layout consistent and intuitive.

### The wireframes:
I created the wireframes using the online tool [Figma](https://www.figma.com/)
The initial wireframes can be viewed [here](https://github.com/kmaaallen/unicorn-attractor-milestone/blob/master/static/wireframes/Figma%20Unicorn.pdf).
I ultimately decided to change the colour scheme during my development process as the dark background was a little too dark for my liking as I was navigating through the site.

### Design decisions
#### Font

- I wanted to keep the design of the site fairly simple so I kept to 'Helvetica Neue' which was the default font style.

#### Colours 

- I also wanted to use web-safe colours where possible to keep the user experience consistent between browsers.
- Using [color-hex](color-hex.com/216-web-safe-colors/) I initially chose a dark web safe colour as my base. Purple, #330066, I did use this in my final design but as an accent colour, by background colour ended up being #f9f9f9, which I still checked for contrast. I also used [sessions](sessions,edu/color-calculator/) to generate a complimentary colour palette which included a green and a pink.
- Using https://www.colortools.net/color_make_web-safe.html I tried to match the green and pink to a web-safe colour and then checked the contrast using a [constrast checker](https://webaim.org/resources/contrastchecker/) to check which colours would work best together according to WCAG AA and WCAG AAA..
- The final colour palette ended up being:
    Purple #330066
    Pink #CC0099
    Green #008500
    White #FFFFFF
    Off White #F9F9F9
- The rest of the palette is made up of two web safe greys.

## Features
### Existing Features
#### Common features (across all pages)

##### Top Navbar (Desktop)
- This site is responsive and as such has two navigation bars. The desktop navigation will display on screen sizes of 993px or wider.
- It always contains the ‘Unicorn Attractor’ logo in the top left corner which is a link back to the homepage when clicked.
- Grouped to the right of the navigation bar (to make viewing easier) are several links that will depend on whether the user is logged in or not.
- If the user is NOT logged in, there will be five links to the right.
    - ‘Find out more' - Will take the user to the 'Find out More' page
    - 'Issues' - Will take the user to the issues overview page
    - 'Sign Up' - Will take the user to the sign up form
    - 'Sign In' - Will take the user to the sign in form.

- If the user IS logged in there will be five links to the right.
    - ‘Find out more' - Will take the user to the 'Find out More' page
    - 'Issues' - Will take the user to the issues overview page - they will now be able to vote on issues and see the 'report an issue' button
    - 'Features' - Will take the user to the feature overview page. If the user is subscribed they will see the 'request a new feature' button and be able
        to vote and comment on existing features. If the user is not subscribed they will see the overview but will not be able to request, vote or comment.
    - '{Username}' - This will show a person icon with the logged in user's username. This takes the user to their profile page.
    - 'Logout' - This logs the user out and redirects them to the sign-in page.

##### Mobile Navbar (Mobile)

- The mobile navbar will display on screens 992px wide or narrower.
- It always contains the ‘Unicorn Attractor’ logo in the top left corner which is a link back to the homepage when clicked. This is consistent with the desktop navigation bar.
- In this nav all links are collapsed under a single menu to the right of the navbar denoted by 'Menu'.
- The same links as described above apply in mobile view.

All links in the navigation bars become underlined when hovered over. This is for consistent styling and so the user can clearly see what they are hovering over whilst remaining subtle enough so as not to distract from the rest of the site.

##### Footer (Mobile and Desktop)
The footer contains three social media icons (instagram, twitter and facebook)
-  As no social media pages exist for this fictional software company, these links currently open their respective social media homepages in a new tab.

##### Landing Page (Homepage)

- Unicorn Attractor Logo
    - Main image
    - Hidden on extra-small and small screens

- Unicorn Attractor main text
    - Clearly states what this website is for.
    - If a user is logged in, above this text there will be displayed: 'Hi {username}, welcome to'

- Enter Button
    - Takes the user to the 'Find out more' page

- Second Button
    - The content of this button will differ depending on whether the user is logged in or not.
    - If the user is not logged in, this button will show 'Sign up/Sign In' and will take the user to the sign up form.
    - If the user is logged in, this button with show 'Logout' and will log the user out and redirect them to the sign in form.


##### Find out more
- The Find out more page contains some text about the fictional software company and contains two buttons.

- Contact Us button
    - This button takes the user to the contact form
    - This contact form allows the user to fill in a name, email and message.
    - Upon submission this form sends an email to the company's email address with the following template:
        Subject: Contact form
        Message:
        {name} has sent you a new message
        {message}
        Their contact email is: {email}

- The second button
    - The content of this button changes depending on which type of user is logged in.
    - If the user is not logged in, it will show 'Sign Up' and will redirect the user to the sign up form
    - If the user is logged in, but is not a subscriber it will show 'Subscribe+' and will redirect the user to the subscription form
    - If the user is logged in and a subscriber it will show 'Manage Subscription' and will redirect the user to their user profile page.

##### User profile page
- This shows the following information:
    {username}'s profile
    Name: {Full name}
    Username: {username}
    Email: {user's email}
    Subscriptions:
- If the user is not subscribed, the profile will say 'Subscriptions: None' and there will be a 'Subscribe+' button underneath
- If the user is subscribed, the profile will say ' Subscriptions: Monthly feature subscription' and there will be two buttons underneath.
    - The first button will say 'Unsubscribe'. Clicking this unsubscribed the user and the profile view changes appropriately.
    - The second button will say 'Update card details'. Clicking this will take the user to the 'Update Card Details' form where they can enter their new card details
    which will then be updated on their Stripe customer account and their next monthly subscription payment will come out of this new card. 
    - Underneath these two buttons is some disclaimer text on when subscription payments will be cancelled for user information as well as a link to the contact form in case users wish to provide feedback on why they are unsubscribing.


##### Password reset page
- Allows a user to enter their email and recieve a link to reset their password for the site

##### Sign in page
- Allows a user to sign in using their username and password

##### Sign up page
- Allows a user to sign up to an account for the site by filling in the following details:
    - First name, last name, username, email, password
    - User has to confirm password and meet password criteria
    - Username has to be unique as does email
    - Email has to be a valid email address

##### Issues page
- This page provides an overview of all the issues reported for the Unicorn Attractor Software.
- The issues are divided between three swim lanes: 'Reported', 'In Progress' and 'Completed'.
- Only admins of the site (i.e. the software developers) can change the state of these issues in the Django admin backend
- Each issue displays the following fields:
    - Title, Issue description, Votes, Priority
    - In addition when a user is logged in, the following links are also displayed:
        - Upvote or the text 'You have laready voted on this issue' if the user has already upvoted, Comments, Add comment
        - Clicking the comments drop down shows a list of comments for that issue or 'No comments yet'
        - Clicking 'Add Comment' redirects the user to the add comment form
        - Whenever a user upvotes an issue, their vote is added to that issue and they are returned to the full issue overview page.
- The page shows a 'Sign in' button on the right if the user is not logged in, this will direct to the sign in form
- If the user is signed in already, this button will say '+ Report and Issue' and direct the user to the report an issue form
- Within swimlanes issues are sorted by which has the highest number of votes. 
- A user can tab between 'My Issues' and 'All Issues' that are displayed in the swimlanes. If not logged in, clicking the 'my issues' will direct the user to sign in.

- Mobile view
    - On small and extra small screens this kanban-style board changes into three toggle buttons, which allow the user to
      select and collapse each of the three swimlanes to see tickets.

##### Full Issue page
- Users can open an issue in a full page view by clicking on the title of that issue.
- This takes them to the full issue view, which contains the same issue components as outlined above but in full page view.
- Whenever a user upvotes an issue they are returned to the full issue overview page.

##### Report an Issue page
- The report an issue page shows a form where a user can enter a title, a description of the issue and assign a priority.
- The choices of priority are LOW, MEDIUM, HIGH and LOW is set by default.
- Underneath the form disclaimer text informs users the priority may be changed by the developers
- Upon submitting an issue the user is redirected to the full issues view.

##### Features page
- This page provides an overview of all the features requested for the Unicorn Attractor Software.
- To access the lowest level of this page users must be logged in.
- To access the full content of this page users must be logged in and subscribed.
- The features are divided between three swim lanes: 'Requested', 'In Progress' and 'Completed'.
- Only admins of the site (i.e. the software developers) can change the state of these features in the Django admin backend
- Each feature displays the following fields:
    - Title, Feature description, Votes, Priority
    - In addition when a user is logged in and subscribed, the following links are also displayed:
        - Upvote or the text 'You have laready voted on this feature' if the user has already upvoted, Comments, Add comment
        - Clicking the comments drop down shows a list of comments for that feature or 'No comments yet'
        - Clicking 'Add Comment' redirects the user to the add comment form
        - Whenever a user upvotes a feature, their vote is added to that issue and they are returned to the feature overview page.
- The page shows a 'Subscribe' button on the right if the user is not subscribed, this will direct to the subscription form
- If the user is subscribed already, this button will say '+ Request a feature' and direct the user to the request a feature form
- Within swimlanes features are sorted by which has the highest number of votes. 
- A user can tab between 'My Features' and 'All Features' that are displayed in the swimlanes.
- These tabs are only visible if the user is subscribed to the features module.

- Mobile view
    - On small and extra small screens this kanban-style board changes into three toggle buttons, which allow the user to
      select and collapse each of the three swimlanes to see tickets.

##### Full Feature Page
- Users can open a feature in a full page view by clicking on the title of that feature.
- This takes them to the full feature view, which contains the same feature components as outlined above but in full page view.
- Whenever a user upvotes a feature they are returned to the feature overview page.

##### Request a Feature page
- The request a feature page shows a form where a user can enter a title, a description of the feature and assign a priority.
- The choices of priority are LOW, MEDIUM, HIGH and LOW is set by default.
- Upon submitting a feature the user is redirected to the all features view.

##### Add comment form
- This form allows users to add a comment to a particular issue or feature.
- The basic form is duplicated across both the issue and features apps and follows the same format.
- The title of the issue/feature is displayed as well as a comment field where a user can add their comment.
- Submitting the form redirects the user to the full issues or full features page respectively.
- The comment if expanded on the ticket will show date of submission, the username of the user who commented and the comment.
- Comments are sorted so that the most recent comments appear at the top.

##### Subscribe form
- The subscribe form allows logged in users to sign up to a monthly subscription managed through Stripe.
- The user can input their card details which will be securely handled by stripe.
- Once subscribed the user sees a message at the top of the subscribe form 'You have successfully subscribed'
- If there are any errors with the card or submititng the form error message will appear.

##### Features Left to Implement
- User profile picture
- Dashboard with data on speed of resolution etc.

## Technologies Used
### Gitpod
This project was written on [Gitpod](https://gitpod.io) using the Code Institute Gitpod template.

### Heroku
This project was deployed using Heroku : [https://id.heroku.com/login](https://id.heroku.com/login">https://id.heroku.com/login)

### Languages
#### Python
Used to write backend functionality in Django application: [https://www.python.org/](https://www.python.org/)

#### JavaScript
Used as a base language to provide functionality and logic :[https://www.w3schools.com/js/default.asp](https://www.w3schools.com/js/default.asp)

#### JQuery
This project uses JQuery to assist in execution of javaScript features:[https://jquery.com/](https://jquery.com/)

#### HTML
Used as a baseline to structure pages:[https://www.w3.org/TR/html/](https://www.w3.org/TR/html/)


#### CSS
Used to style pages:[https://www.w3.org/Style/CSS/Overview.en.html](https://www.w3.org/Style/CSS/Overview.en.html)


#### Django Template Language
Used as a templating language with Python to render HTML on site:[https://docs.djangoproject.com/en/3.0/ref/templates/language/](https://docs.djangoproject.com/en/3.0/ref/templates/language/)

### Validators
Online validators were used to check code was valid for HTML and CSS and to help catch errors in Javascript and Python.
- HTML validator:[https://validator.w3.org](https://validator.w3.org">https://validator.w3.org)
- CSS Validator:[http://jigsaw.w3.org/css-validator/](http://jigsaw.w3.org/css-validator/)
- JavaScript correction tool:[https://jshint.com/](https://jshint.com/)
- Python validator:[http://pep8online.com/checkresult](http://pep8online.com/checkresult)

### Libraries
#### Bootstrap
Used to build a responsive site:[https://getbootstrap.com/](https://getbootstrap.com/)

#### Icons

### Frameworks
#### Django
Web framework used to construct and render pages and to run automated tests:[https://www.djangoproject.com/](https://www.djangoproject.com/)

### Payement Platform
#### Stripe 
I used the Stripe payment platform to collect subscriptions from users, available here: [https://stripe.com/gb](https://stripe.com/gb)

### Version control
Git was used for version control and a local git repository was pushed to a remote repository on GitHub:

[https://git-scm.com/](https://git-scm.com/)

[https://github.com/](https://github.com/)

### Tools
An online favicon generator was used to create a favicon for my site.The favicon image can be viewed [here](https://github.com/kmaaallen/bake_book/blob/master/static/favicon.ico).

The online generator tool is available at: [https://www.favicongenerator.com/](https://www.favicongenerator.com/)

### Database
MongoDB Atlas was used as the database for this project :[https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)

## Testing

### Manual Testing
The manual testing document can be viewed [here](https://github.com/kmaaallen/unicorn-attractor-milestone/blob/master/unicorn_attractor/Documentation/Manual%20Testing%20Unicorn%20Attractor.xlsx)

#### Interesting bugs / bugs not fixed

### Automated testing
I used Django's automated testing framework.

#### What was tested:
I tested the following and achieved the following coverages with automated testing:

ISSUES:
Coverage report: 99%
Module	            statements	missing	    excluded	coverage
issues/admin.py	        5	        0	        0	        100%
issues/apps.py	        3	        0	        0	        100%
issues/forms.py	        10	        0	        0	        100%
issues/models.py	    36	        0	        0	        100%
issues/test_app.py	    7	        0	        0	        100%
issues/test_forms.py	43	        0	        0	        100%
issues/tests.py	        60	        0	        0	        100%
issues/urls.py	        3	        0	        0	        100%
issues/views.py	        53	        3	        0	        94%
Total	                386	        3	        0	        99%

Name                                           Stmts   Miss  Cover
------------------------------------------------------------------
issues/__init__.py                                 0      0   100%
issues/admin.py                                    5      0   100%
issues/apps.py                                     3      0   100%
issues/forms.py                                   10      0   100%
issues/models.py                                  36      0   100%
issues/test_app.py                                 7      0   100%
issues/test_forms.py                              43      0   100%
issues/tests.py                                   60      0   100%
issues/urls.py                                     3      0   100%
issues/views.py                                   53      3    94%
------------------------------------------------------------------
TOTAL                                            386      3    99%

Name                                              Stmts   Miss  Cover
---------------------------------------------------------------------
features/admin.py                                     5      0   100%
features/apps.py                                      3      0   100%
features/forms.py                                    10      0   100%
features/models.py                                   34      0   100%
features/test_apps.py                                 7      0   100%
features/test_forms.py                               47      0   100%
features/tests.py                                    82      1    99%
features/urls.py                                      3      0   100%
features/views.py                                    53      4    92%
---------------------------------------------------------------------
TOTAL                                               270      5    98%

Name                              Stmts   Miss  Cover
-----------------------------------------------------
accounts/admin.py                     1      0   100%
accounts/apps.py                      3      0   100%
accounts/forms.py                    28      0   100%
accounts/models.py                    1      0   100%
accounts/test_apps.py                 7      0   100%
accounts/test_forms.py               81      0   100%
accounts/tests.py                    50      0   100%
accounts/url_reset.py                 4      0   100%
accounts/urls.py                      4      0   100%
accounts/views.py                    38      1    97%
-----------------------------------------------------
TOTAL                               217      1    99%

Name                              Stmts   Miss  Cover
-----------------------------------------------------
home/admin.py                         1      0   100%
home/apps.py                          3      0   100%
home/forms.py                         6      0   100%
home/models.py                        5      0   100%
home/test_apps.py                     7      0   100%
home/test_forms.py                   25      0   100%
home/tests.py                        35      0   100%
home/urls.py                          3      0   100%
home/views.py                        24      0   100%
-----------------------------------------------------
TOTAL                               115      0   100%

SUBSCRIPTIONS MODULE TO GO IN HERE WHEN TESTS DONE
#### How to run these tests
In order to run these tests you must use the project locally and in your environment variables comment out the postgres database and use the sqlite database that comes with django.
You must also pip3 install coverage
To generate the reports run the following command: $ coverage run --source='<app-name>' manage.py test <app-name>
Then $ coverage report

## Deployment
### How to deploy this project to Heroku
1. Go to the Heroku website (https://id.heroku.com/login) and login to your account.
2. Create a new application by clicking “New” in your dashboard. Name this app and set the region to Europe.
3. Configure the deployment option for your app to be direct from GitHub and link to your repository containing the project code.
4. Set configuration variables in Heroku by going to the ‘settings’ section of your application. Set them as follows:

- IP	0.0.0.0
- PORT	5000
- DATABASE_URL
- EMAIL_ADDRESS
- EMAIL_PASSWORD
- SECRET_KEY
- STRIPE_PUBLISHABLE
- STRIPE_SECRET

- In order to deploy to Heroku you need to make sure your project has a requirements.txt file
- Create by running the following command in your terminal:
 > pip freeze –local  > requirements.txt
- You will also need a Procfile
    - Create by running the following command in your terminal:
> Echo web: python app.py > Procfile (where app.py is the name of your python file for the app.
- Add, commit and push those additions to your GitHub repo

### How to run this project locally
- 

## Credits
### Content

### Media

## Acknowledgements
