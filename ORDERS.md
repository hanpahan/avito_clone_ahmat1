# Orders API

Run `run.py` or `main.py`, then open http://127.0.0.1:8001/docs.
Stop the previous server before starting the updated application.
The orders table is created automatically during startup in the configured SQL Server database.

| Method | Route | Function |
| --- | --- | --- |
| GET | /orders | get_all_order |
| GET | /orders/{order_id} | get_order |
| POST | /orders | post_order |
| PUT | /orders/{order_id} | put_order |
| DELETE | /orders/{order_id} | delete_order |

POST body (user 1 must exist):

```json
{"name": "Keyboard", "user_id": 1, "price": "2500.00"}
```

PUT accepts any subset of name, user_id and price. Explicit null values are rejected.
Price must be nonnegative, with up to 10 integer digits and 2 decimal places.
Responses serialize decimal prices as strings to preserve precision.
Missing orders or referenced users return 404. Successful deletion returns 204.
A user with orders cannot be deleted (409); delete their orders first.

Verification: all 8 automated tests passed, covering users and orders CRUD,
validation, missing references, ownership changes, foreign key protection,
rollback, Swagger and all 10 operations. Tests use isolated in-memory SQLite
with foreign keys enabled; production configuration remains Microsoft SQL Server.
Run: `python -m unittest discover -s tests -v` after installing requirements-dev.txt.

Live SQL Server startup from the agent process failed with Windows error
0x8009030E (missing security credentials). Actual SQL Server CRUD is unverified.
