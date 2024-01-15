# 253B Final Project Write-Up ~ Group 10 #
## **Team Members:** Erin Jones, Sathvik Kolli, Sihang Liu, Grace Roseman, Pranjal Sinha ##

**What was your original goal and how much of it were you able to achieve?** <br>
Our high-level goal was to build multiple APIs that interact with each other and a database. More specifically, we wanted to create a user API, which handles registration, authentication, log-in, and session management for users, and other content API's which provide the user with access to a wide range of content types: news, financial time series, horoscope data, a restaurant dashboard, and more. 

With regards to the user API, we originally planned to have a user registration endpoint which would receive a username, password, email address, and the user's content preferences (e.g. what kind of content they want? how frequently they want email updates?) and store these in a table in our database. We planned to use some sort of account verification system, potentially using the SendGrid external API. Finally, we also wanted to provide a login page enabling the user to log-in and maintain a persistent session.

For the content API's, we planned to have a user-personalized home page with links to multiple dashboards serving different types of content. Each content API would live in a different Docker container and be hosted on a different port. We wanted to personalize the content to the user's preferences and to store data on the user's interaction with the content in our database.

We were able to achieve the majority of our goal. We did create a user registration page, a login page, support for user authentication along with account verification using SendGrid, and persistent sessions using FlaskSession. However, we decided not to ask users for their content preferences during registration, as it offered users more freedom to explore the data provided by the integrated API. Integrating preferences would also have led us into the territory of building a center whereby a user might modify preferences, which we did not have time to implement. Avoiding user preference at registration also allowed for greater ease of integration, as our team each wrestled with different APIs and having user preference impact some but not others would have necessitated the creation of two types of service containers that interacted with the flask sessions. The finance API does integrate the storage of previously searched tickers that are stored within a database table, which would allow the user to quickly reproduce their search activity in the future. We also built a home page linking to different content pages. We did adjust which external APIs we used and content pages we created, based on the external APIs we found (e.g. the horoscope API was more difficult to source than we had originally imagined).

**A description of what your project does and the functionality that it provides**<br>
*Overview:*
- Application Built: A website that allows users to register/log-in and to access content dashboards that the user can explore based on their interests and preferences: Finance, Pokemon, News, Street View, and Weather 
- External APIs: SendGrid, Nasdaqdatalink, pokeapi, newsapi, Google Street View Static API, OpenWeatherMap API
- Database: Stores user data (username, hash of password, email, and verification status) as well as all user queries on the Finance Dashboard
- Docker Containers and Volumes: We have 1 container for our Postgres Database, 1 container for our user API and home page (port 5050), and 4 containers for each content API: financial API (port 5051), pokemon API (port 5052), news API (port 5053), streetview API (port 5054), and weather API (port 5055). We also have two persistent volumes: one for our database and one for persistent flask sessions that are accesible across all docker containers.

*Description:* <br>
The homescreen of our website has several dashboards the user can access: Finance, Pokemon, News, Street View, and Weather. Before having access to these dashboards, the user must register an account with their username, email, and password. After registering an account, an email is sent using SendGrid that prompts the user to click on a link to verify their account. Once an account is verified, the user can login to the site and access the various dashboards.

In the Finance Dashboard, the user can enter a symbol to get a graph that shows the financial data from Nasdaq. The previous symbols that were looked up by the user are stored in a table and displayed to the user on this page.

In the Pokemon Dashboard, the user can input a Pokemon name and the site then returns images of the Pokemon with its description. 

In the News Dashboard, the user can enter a country code to get a table with the top daily news articles for that country with their links, which are opened automatically in a new tab when clicked.

In the Street View Dashboard, the user can enter a location to get street view images associated with that location. 

In the Weather Dashboard, the user can enter a zipcode and corresponding country code to get shown the current weather in degrees Fahrenheit for that location. 

While in any dashboard, the user can hit the "home" button to be navigated back to the homescreen with all of the dashboard options. The user can also logout at any time. 

**What did you learn from the project? Talk about the mistakes you made, challenges you overcame or the tools that you got to learn etc**
- We gained valuable experience working with a wide range of external APIs.
- We learned that different external APIs require different workflows for integration. It was a bit challenging at times to learn how to integrate an unfamiliar external API since different APIs return data in different forms which took us a bit of time to learn how to work with it. Our approach of allowing team members to work with their API independently prior to integrated resulted in novel methods of integration within the user app - e.g. the plotting of API data to a static image displayed for the user, the return of direct text from the API, the writing of API JSON data into an html file to be stored statically
- We learned how to use FlaskSession to maintain persistent user sessions. This was an excellent dissemination of knowledge and skills, whereby some team members had more coding experience than others and nimbly produced an implementation, which was then absorbed by other team members.
- We learned the basics of building a user authentication API, and we learned how to hash passwords rather than storing them in plain-text in our database.
- We learned how to build a modular application which can be easily extended and modified by multiple engineers to integrate new API types.
- We had some challenges with ensuring that our code worked for all of us, and we learned the importance of resolving ambiguities in the requirements.txt file by explicitly specificing versions. 
- We also unexpectedly learned some frontend because of our desire to have a working frontend for our demo.
- We learned about HTTP codes in the context of flask redirect i.e. you can't add a code without the system throwing an error and must instead rely on the system's automatic 300 code
- While the approach of allowing each individual to leverage their existing skills and play with an API of interest, the resulting output did appear less cohesive when compared with other team's efforts. The structure did lend itself well to remote coordination of team members with varying skill levels, allowing all members to contribute to the code and functionality while requiring few in person meetings. In the context of this project, it is not a good or a bad thing, but in the future, it is an important strategy consideration when examining desired user interactions with the system.
- We made good use of classroom skills that required the examination of example code, modification and then implementation to create a unique solution. The integration of many services hinged on our ability to "plug and play" within the user framework that was created, which was the basis for meeting the requirements of the group project. At times, it may have been beneficial to have greater levels of documentation within the code, however this was overcome via communication and team member willingness to step in and help out when resolving errors.
- Overall, this project gave us good experience with the class material, and we didn't encounter many significant challenges thanks to the great course material/instruction which we all felt gave us a good understanding of and foundation for back-end development.
