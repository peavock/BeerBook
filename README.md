1. What goal will your website be designed to achieve?
> - The goal is to create a social network where users can keep track of breweries / beers they have visited / had, to be able to write reviews of both, share recommendations with others, and put together a bucket list of beers / breweries they would like to have / visit.

2. What kind of users will visit your site? In other words, what is the demographic of your users?

	> - Anyone who enjoys craft beers. This demographic would likely skew male, but age-wise would include anyone 21 or over.

3. What data do you plan on using?

	> - I would like to use the Brewery DB database (although only the sandbox version is available for free, but it does appear to have a good amount of beers available and a small list of breweries)

4. In brief, outline your approach to creating your project:
	- What does your database schema look like:
 		- User table with information about users
 		- Beers table with information about beers and brewery\_id
 		- Breweries table with information about breweries
 		- Beers\_tried - table with beers tried by users association
 		- Breweries\_tried - table with breweries tried by users association
		- Beers\_liked - table with beers liked by users association
   		- Breweries\_liked - table with breweries liked by users association
    	- Beer\_Reviews - table with beer reviews including author user\_id
    	- Brewery\_Reviews - table with brewery reviews including author user\_id
	- What kind of issues might you run into with your API?
    	- Limited data in the sandbox version
    	- Getting exact name matches for beers and breweries
 	- Is there any sensitive information you need to secure?
    	- User log-in password, but otherwise not really
    	- Users should only be able to edit / delete their own content
  - What functionality will your app include
    	- At the website, you can create a username / login using authentication
    	- Once logged in, as part of your profile it will show the # of breweries you have visited, # of beers you have tried, and # of reviews you have written
    	- You can search Brewery DB for breweries / beers and indicate that you have had them OR that you want to try them
      		- For beers / breweries that you have had you can fill out a review and put them on your favorites list
    		- There will be a separate page listing breweries / beers the user wants to try (bucket list)
    		- There will be pages with detail on each:
      			- Brewery with it&#39;s beers, # reviews, # of visitors, # times favorited, and a few recent reviews
      			- Beers with # tries, # times favorited, # reviews and a few recent reviews
- What will the user flow look like:
	- Users
		- Sign-Up: show sign-up form
		- Log-In: show log-in form
		- Home Page: show profile details
			- \# beers tried
			- \# breweries visited
			- \# reviews written
			- \# 5 most recent reviews
		- Nav Bar
			- Favorite Beers
			- Favorite Breweries
			- Tried Beers (show a togglable star for favorite)
			- Tried Breweries (show a togglable star for favorite)
			- Wish List Beers
			- Wish List Breweries
			- My Reviews
			- Write a Review
	- Breweries
		- \# beers available
		- \# visitors
		- \# times favorited
		- \# reviews received
		- 5 most recent reviews
		- All beers with \# favorites indicated
	- Beers
		- Beer home page with page details
		- Any pertinent beer info
		- Brewery info
		- \# reported tries
		- \# times favorited
		- \# reviews received
		- 5 most recent revieews
	- Review Pages
		- Show the review content, including author
		- Allow to follow the author to see other reviews
