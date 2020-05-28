# Paper analyzer relations viewer

## Running the server
Call `make run-production` to run a server.

## Adding a collection of relations

The collection of relations should be added to `data/databases/$COLLECTION_NAME/relationds.db`. 
Run `make run-preprocessing` to preprocess the collections and cache files needed for server.

The database with extracted relations could be downloaded from [here](https://drive.google.com/open?id=13ECQHnNMcJXqxHAIJJwNu5s7drHXL0Sa).
I will host this database on a server in the future.

## Debugging
Run server with `make run-debug`, then go to client directory and call `yarn start` to run UI in debug mode.

