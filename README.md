# HomeCooksGalore
Home Cooks Galore is a social network website for home cooks that allows people to share personal recipes of home-made dishes with the world, learn from others and build a network in the process. 

Technologies used were Django and AJAX ( backend ) and Bootstrap 4 ( frontend )

![Home Page](https://github.com/tusharsircar95/HomeCooksGalore/blob/master/HCGImages/homepage.JPG)


## Features

#### User registration, authentication and login
Allows new users to register with a unique username and password ( only encrypted passwords are stored for security purposes ). Existing users may login using their credentials to access their profile, upload recipes and view other recipes.

#### Allows signed in users to upload/edit/delete their recipes
Signed in users can upload their own recipie to share with others. Each recipie may belong to either FOOD or DRINK category, has a set of instructions and an image. A user can edit or delete his existing recipes as well.

![Dish Details Page](https://github.com/tusharsircar95/HomeCooksGalore/blob/master/HCGImages/dishdetailspage.JPG)

![Edit Page](https://github.com/tusharsircar95/HomeCooksGalore/blob/master/HCGImages/editpage.JPG)


#### Permission system so that users can only modify their own recipes
Only signed in users can view recipes shared by others. Also, only the publisher of a recipie may edit/delete it, other users only have the permission to view it. This is to make sure that unauthorized users may not modify recipes.

#### Search functionality that allows users to search for particular dishes using keywords
Users can enter a query in the search bar and corresponding dishes are fetched from the database and displayed. Presently, search checks for dishes that contain the keyword provided in their dish name.

![Search Page](https://github.com/tusharsircar95/HomeCooksGalore/blob/master/HCGImages/searchpage.JPG)


#### Follow / Unfollow capability
User may follow/unfollow other users. This will allow to customize the newsfeed accordingly (future work). The follow/unfollow button UI transition and the updates to the page once a follow/unfollow action is made, is done using AJAX, so that the page need not be refreshed. (similar to facebook likes or instagram follows)


#### Like / Unlike capability for posts, ratings for each dish
User may like (or unlike a liked post) posted dishses. Each dish has a corresponding rating which is the number of people that have liked it. Each user can like a particular dish just once. Like the follow/unfollow feature, the like action is also done via AJAX.

#### Messaging system
Users may send messages to other users by going to their profile and clicking the Message button. A user may go to the messages tab to view a summary of all conversations he has had. Each conversation summary displays the user with which the conversation is, the last message of the conversation and the time of the last message.
User may decide to view all messages in the conversation as well.

![Message Summaries](https://github.com/tusharsircar95/HomeCooksGalore/blob/master/HCGImages/msgsummarypage.JPG)

![Message Details](https://github.com/tusharsircar95/HomeCooksGalore/blob/master/msgdetailspage.JPG)

#### Profile Page
Profile page that displays all recipes shared by a user and also the number of recipes posted, number of followers and the number of users followed by the user.

![Profile Page](https://github.com/tusharsircar95/HomeCooksGalore/blob/master/HCGImages/profilepage.JPG)

#### AJAX Support
Whenever a button is clicked and a small portion of the webpage needs to be refreshed, instead of refreshing the entire webpage, AJAX is used to update only the necessary part, resulting in a better and smoother experience.


## UI Improvements
Most work done so far is on the backend functionality. UI/UX needs to be improved. Following are just few points tht can be worked upon:

- Cards to display recipes often end up one below the other (all in one column)

- Login/Registration page revamp

- Fonts

- Chat windows for messaging

## Future Features
- Real-time messaging system
- Recommendation system to suggest recipes to users 

