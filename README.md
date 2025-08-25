database -> location to store db 
models -> table we want to be stored in db

CRUD in sql


Create -> `isnert into todos (title, desc, priority, complete) values ('go to store', 'to do xyz', 5, False)` -> false is considered 0 in sql
Read -> `select * from todos where id=5`
Update -> `update todos set title='hey' where id=5`
Delete -> `delete from todos where id=5`


Different ways to connect to db 
we will be using sqlalchemy engine -> that powers our connection

```
format: driver+postgresql://user:pass@host:port/dbname
DB_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="user",
    password="pass",
    port=5432,
    database="testDb",
)
```

`engine = create_engine(DB_URL, echo=True)`


