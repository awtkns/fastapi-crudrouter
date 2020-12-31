## Default Routes
By default, the CRUDRouter will generate the six routes below for you. 

| Route        | Method   | Description
| ------------ | -------- | ----
| `/`          | `GET`    | Get all the resources 
| `/`          | `POST`   | Create a new resource 
| `/`          | `DELETE` | Delete all the resources
| `/{item_id}` | `GET`    | Get an existing resource matching the given `item_id`
| `/{item_id}` | `PUT`    | Update an existing resource matching the given `item_id`
| `/{item_id}` | `DELETE` | Delete an existing resource matching the given `item_id`

!!! note "Route URLs"
    Note that the route url is prefixed by the defined prefix.

    **Example:** If the CRUDRouter's prefix is set as *potato* and I want to update a specific potato the route I want to access is
    `/potato/my_potato_id` where *my_potato_id* is the ID of the potato.

## Prefixes
Depending on which CRUDRouter you are using, the CRUDRouter will try to automatically generate a suitable prefix for your
model.  By default, the [MemoryCRUDRouter](backends/memory.md) will use the pydantic model's name as the prefix.  However,
the [SQLAlchemyCRUDRouter](backends/sqlalchemy.md) will use the model's table name as the prefix.

!!! tip "Custom Prefixes"
    You are also able to set custom prefixes with the `prefix` kwarg when creating your CRUDRouter. This can be done like so:
    `router = CRUDRouter(model=mymodel, prefix='carrot')`

## Disabling Routes
Routes can be disabled from generating with a key word argument (kwarg) when creating your CRUDRouter. The valid kwargs 
are shown below.

| Argument         | Default | Description 
| ---------------- | ------  | ---
| get_all_route    | True    | Setting this to false will prevent the get all route from generating
| get_one_route    | True    | Setting this to false will prevent the get one route from generating
| delete_all_route | True    | Setting this to false will prevent the delete all route from generating
| delete_one_route | True    | Setting this to false will prevent the delete one route from generating
| create_route     | True    | Setting this to false will prevent the create route from generating
| update_route     | True    | Setting this to false will prevent the update route from generating