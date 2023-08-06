# Summary
Converts [SQLAlchemy](https://www.sqlalchemy.org/) models to [AtlasGo](https://atlasgo.io/) HCL.

# Quickstart
<!-- Installation -->
- Run `pip install sqlalchemy2atlas`
<!-- Usage -->
- Run `sqlalchemy2atlas -h`


## Driver Support
- [x] PostgreSQL
    - [x] 14.x
- [ ] Cloud Spanner
- [ ] MySQL
- [ ] SQLLite


# Example
Example of converting a SQLAlchemy module into AtlasGo HCL.

```python
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    CheckConstraint,
    ForeignKey,
)

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    # Feat: Primary Key
    id = Column(Integer, primary_key=True)

    # Feat: Column Types
    name = Column(String(30))
    full_name = Column(String)
    age = Column(Integer)

    # Feat: Check Constraints
    check_age_positive = CheckConstraint(age > 0)
    check_age_reasonable = CheckConstraint(age < 200)

class Account(Base):
    __tablename__ = "account"

    # Feat: Primary Key
    id = Column(Integer, primary_key=True)

    # Feat: Column Types, Foreign Keys
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    account_created_at = Column(DateTime, nullable=False)

```

Into

```go
table "account" {
  schema = schema.public
  column "id" {
    null = false
    type = serial
  }
  column "user_id" {
    null = false
    type = integer
  }
  column "account_created_at" {
    null = false
    type = timestamp
  }
  primary_key {
    columns = [column.id]
  }
  foreign_key "account_user_id_fkey" {
    columns     = [column.user_id]
    ref_columns = [table.user.column.id]
    on_update   = NO_ACTION
    on_delete   = NO_ACTION
  }
}
table "user" {
  schema = schema.public
  column "id" {
    null = false
    type = serial
  }
  column "name" {
    null = true
    type = character_varying(30)
  }
  column "full_name" {
    null = true
    type = character_varying
  }
  column "age" {
    null = true
    type = integer
  }
  primary_key {
    columns = [column.id]
  }
  check "user_age_check" {
    expr = "(age > 0)"
  }
  check "user_age_check1" {
    expr = "(age < 200)"
  }
}
schema "public" {
}
```