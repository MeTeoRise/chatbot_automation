There was a problem in YAMLField where:
```bash
from_db_value() missing 1 required positional argument: 'context'
```

It was solved by updating `~/.local/lib/python3.8/site-packages/yamlfield/fields.py` from_db_value() to:
```python
def from_db_value(self, value, expression, connection, context=None):
        return self.to_python(value)
```