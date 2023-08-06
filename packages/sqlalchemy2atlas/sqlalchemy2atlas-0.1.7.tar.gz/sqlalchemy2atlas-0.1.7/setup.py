# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy2atlas']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4,<2.0', 'docker>=6.0,<7.0', 'psycopg2>=2.9,<3.0']

entry_points = \
{'console_scripts': ['sqlalchemy2atlas = '
                     'sqlalchemy2atlas.sqlalchemy2atlas:main']}

setup_kwargs = {
    'name': 'sqlalchemy2atlas',
    'version': '0.1.7',
    'description': 'Converts SQLALchemy Base Classes to AtlasGo HCL.',
    'long_description': '# Summary\nConverts [SQLAlchemy](https://www.sqlalchemy.org/) models to [AtlasGo](https://atlasgo.io/) HCL.\n\n# Quickstart\n<!-- Installation -->\n- Run `pip install sqlalchemy2atlas`\n<!-- Usage -->\n- Run `sqlalchemy2atlas -h`\n\n\n## Driver Support\n- [x] PostgreSQL\n    - [x] 14.x\n- [ ] Cloud Spanner\n- [ ] MySQL\n- [ ] SQLLite\n\n\n# Example\nExample of converting a SQLAlchemy module into AtlasGo HCL.\n\n```python\nfrom datetime import datetime\nfrom sqlalchemy.orm import declarative_base\nfrom sqlalchemy import (\n    Column,\n    Integer,\n    String,\n    DateTime,\n    CheckConstraint,\n    ForeignKey,\n)\n\nBase = declarative_base()\n\nclass User(Base):\n    __tablename__ = "user"\n\n    # Feat: Primary Key\n    id = Column(Integer, primary_key=True)\n\n    # Feat: Column Types\n    name = Column(String(30))\n    full_name = Column(String)\n    age = Column(Integer)\n\n    # Feat: Check Constraints\n    check_age_positive = CheckConstraint(age > 0)\n    check_age_reasonable = CheckConstraint(age < 200)\n\nclass Account(Base):\n    __tablename__ = "account"\n\n    # Feat: Primary Key\n    id = Column(Integer, primary_key=True)\n\n    # Feat: Column Types, Foreign Keys\n    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)\n    account_created_at = Column(DateTime, nullable=False)\n\n```\n\nInto\n\n```go\ntable "account" {\n  schema = schema.public\n  column "id" {\n    null = false\n    type = serial\n  }\n  column "user_id" {\n    null = false\n    type = integer\n  }\n  column "account_created_at" {\n    null = false\n    type = timestamp\n  }\n  primary_key {\n    columns = [column.id]\n  }\n  foreign_key "account_user_id_fkey" {\n    columns     = [column.user_id]\n    ref_columns = [table.user.column.id]\n    on_update   = NO_ACTION\n    on_delete   = NO_ACTION\n  }\n}\ntable "user" {\n  schema = schema.public\n  column "id" {\n    null = false\n    type = serial\n  }\n  column "name" {\n    null = true\n    type = character_varying(30)\n  }\n  column "full_name" {\n    null = true\n    type = character_varying\n  }\n  column "age" {\n    null = true\n    type = integer\n  }\n  primary_key {\n    columns = [column.id]\n  }\n  check "user_age_check" {\n    expr = "(age > 0)"\n  }\n  check "user_age_check1" {\n    expr = "(age < 200)"\n  }\n}\nschema "public" {\n}\n```',
    'author': 'Fraser Isbester',
    'author_email': '28307321+Fraser-Isbester@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
