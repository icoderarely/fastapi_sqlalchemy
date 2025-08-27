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

JWT -> JSON web tokens
a way to securely transmit data and info between two parties using json object
it can be trusted because each jwt can be digitally signed -> allows server to know if data was changed in between or not
should
 not an authentication methods like -> 

authorization method which maintain relationship b/w client and server without loggin everytime sending a request

once user logs in, the server returns a json web token -> a string of characters
created by three sepeare parts, ,seperated by dots -> `aaaa.bbbb.cccc`

aaaa -> header 
    two parts: algorithm for signing "alg", and the type of token "typ"
    then encoded using base64 to create first part
bbbb -> payload
    consists of the actual data and or additional info
    contains claims
        1. register: predifined, recommended but not manditory -> iss, sub, exp (is this of register? explain agent each and wher does this belong put it there)
        2. public: 
        3. private: 
    then is encoded using base 64 for second part
cccc -> signature
    created by algo stated in header -> to hash out the encoded header, encoded payload with a secret
    secret can be anything, saved on server but, client have no access to 


