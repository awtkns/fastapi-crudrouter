The CRUDRouter is set up to automatically paginate your routes for you. You can use the `skip` and `limit` query parameters to
paginate your results.

**Skip**:
Using the `skip` (int) parameter, you can skip a certain number of items before returning the items you want.

**Limit**:
Using the `limit` (int) parameter, the maximum number of items to be returned can be defined.

!!! tip "Setting a Maximum Pagination Limit"
    When creating a new CRUDRouter you are able to set the maximum amount of items that will be returned per page.
    To do this, use the `paginate` kwarg when creating a new CRUDRouter as shown in the example below.

    ```python
    CRUDRouter(
        schema=MyPydanticModel, 
        paginate=25
    )
    ```

    Above a new CRUDRouter is being created that will paginate items at 25 items per page.


### Example
Shown below is an example usage of pagination; using `skip` and `limit` to paginate results from the backend. More information on how to 
`skip` and `limit` can be used with fastapi can be found [here](https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils).

=== "Python"

    ```python
    import requests

    requests.get('http://localhost:5000/potatoes' params={
        'skip': 50,
        'limit': 25
    })
    ```

=== "Bash"

    ```bash
    curl -X GET -G \
    'http://localhost:5000/potatoes' \
    -d skip=50 \
    -d limit=25
    ```

In the example above, 25 items on the third page are being returned from our fictitious CRUDRouter endpoint. It is the third
page because we specified a `skip` of 50 items while having a `limit` of 25 items per page. If we were to want items on the fourth 
page we would simply have to increase the `skip` to 75.



### Validation
CRUDRouter will return HTTP Validation error, status code 422, if any of these conditions are met:

- The skip parameter is set to less than 0
- The limit parameter is set to less than 1
- The limit parameter is set to more than the maximum allowed number of records if a maximum is specified.

Shown below is a sample validation error. In the example, a negative value for the `skip` parameter was supplied.
```json
{
  "detail": {
    "detail": [
      {
        "loc": ["query", "skip"],
        "msg": "skip query parameter must be greater or equal to zero",
        "type": "type_error.integer"
      }
    ]
  }
}
```





