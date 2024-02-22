# Turso, htmx, and Flask demo

Implementation and notes of the demo project at https://blog.turso.tech/creating-a-website-using-htmx-and-turso-7727d396ef77

## Setup

### Creating and using a Turso db

```shell
# create a new db
turso db create [db-name]

# get the db url
turso db show - url [db-name]

# create a token
turso db tokens create [db-name]
```

### Generate `.env`

`$ ./scripts/configure_env`
