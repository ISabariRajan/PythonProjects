import facebook

# Replace with your own access token
access_token = 'EAANMXVqZBKKgBANYRE7ZBXHbMdiCKNDnSuiQM1ijLMJaVpw5JNZAM7XZArvDGZC3wXTNaXq48mfFFnp9LA1lhZBhMAyJAYKNwYC478zuMcqFHgQoLR6eK9pF5HY2uZA4ja817BjWDhypZBsrzqUNXjFnGVneGDmVCSEm2Cz8SNhyZAl2YBzonKRUVZB3JPiCefLTkpQ0ZARJ6ghNZBxVgRmtRWQQ8pQjZC7DAZAN8H98wNt5QzMBWlr5aGpYIz'

# Replace with the Facebook ID of the person you want to extract comments and posts from
user_id = "3498288857090919"

# Create a Facebook Graph API object
graph = facebook.GraphAPI(access_token=access_token, version='3.1')

# Extract the person's posts
posts = graph.get_connections(id=user_id, connection_name='posts')

# Print the post messages
for post in posts['data']:
    print(post['message'])

    # Extract the post comments
    comments = graph.get_connections(id=post['id'], connection_name='comments')

    # Print the comment messages
    for comment in comments['data']:
        print('- ' + comment['message'])

# "https://graph.facebook.com/v16.0/3498288857090919?access_token=EAANMXVqZBKKgBANYRE7ZBXHbMdiCKNDnSuiQM1ijLMJaVpw5JNZAM7XZArvDGZC3wXTNaXq48mfFFnp9LA1lhZBhMAyJAYKNwYC478zuMcqFHgQoLR6eK9pF5HY2uZA4ja817BjWDhypZBsrzqUNXjFnGVneGDmVCSEm2Cz8SNhyZAl2YBzonKRUVZB3JPiCefLTkpQ0ZARJ6ghNZBxVgRmtRWQQ8pQjZC7DAZAN8H98wNt5QzMBWlr5aGpYIz"