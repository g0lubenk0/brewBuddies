
# BrewBuddies
BrewBuddies is a social platform that brings beer enthusiasts together. Connect with like-minded individuals, create and join beer-tasting groups, and share your favorite brews.

## Features
**Group Creation** : Users can create beer-tasting groups, providing details such as the group name, location, description, and tags.

**Group Joining/Leaving**: Join existing beer-tasting groups or leave those you've joined. Manage your group memberships effortlessly.

**Group Updates**: Group creators can update the details of their groups, ensuring the information is always accurate.

**Group Deletion**: Group creators have the option to delete groups they've created.

**Group Chat**: Engage in lively conversations with fellow group members through the group chat feature.

**Location-based Search**: Find beer-tasting groups based on location, making it easy to connect with local enthusiasts.

**Map Integration**: A visual map displays all existing beer-tasting groups, allowing users to explore and discover groups in their area.

**User Profile**: Each user has a profile where they can add personal details, a profile image, and a short bio.

## Installation
Clone the repository:
````
git clone https://github.com/your-username/brewBuddies.git
````

Navigate to the project directory:
````
cd brewBuddies
````

Install dependencies:
````
pip install -r requirements.txt
````

**OR** using Poetry:
````
pip install Poetry
poetry install
````

Apply database migrations:
````
python manage.py migrate
````

Run the development server:
````
python manage.py runserver
````

To run with chat, you need to install docker then:
````
daphne brewbuddies.asgi:application
````
Visit http://localhost:8000/ in your web browser to access BrewBuddies.

## Usage
**Create an Account**: Sign up for a BrewBuddies account or log in if you already have one.

**Explore Groups**: Browse existing beer-tasting groups or use the search feature to find groups based on tags or location.

**Create a Group**: Start your own beer-tasting group and invite others to join.

**Join/Leave Groups**: Join groups that interest you or leave groups you no longer wish to be a part of.

**Group Chat**: Participate in group chats to discuss your favorite beers, upcoming events, and more.

**Update/Delete Groups**: If you created a group, you can update its details or delete the group if necessary.

**Map View**: Explore the map to see the geographical distribution of beer-tasting groups.

## Contributing
We welcome contributions to make BrewBuddies even better! Feel free to open issues, submit pull requests, or suggest new features.

## Getting Started with Development
Fork the repository. Clone your forked repository:

````
git clone https://github.com/your-username/brewBuddies.git
````

Create a new branch for your changes:
````
git checkout -b feature/new-feature
````

Make your changes, commit them, and push to your fork:
````
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
````

Create a pull request from your fork to the main repository.
