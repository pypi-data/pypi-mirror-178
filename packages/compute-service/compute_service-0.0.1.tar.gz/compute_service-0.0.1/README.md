# Compute Service

This is a Python library to create Compute Service with REST API and task queue.

## Usage

To create new compute service one need to:

1. Import packages
```
from pydantic import BaseModel
from compute_service import ComputeService
```
2. Create service object with selected queue type:
```
service = ComputeService(queue='kafka')
``` 
`kafka` and `local` queue types are supported.

3. Define model for input parameters and app factory:
```
class UserBase(BaseModel):
    title: str
    value: int

def create_app():
    return service.create_app(UserBase)
```

4. Define task processing callback and task handler:
```
def process(data):
    print(f'Got data: {data}')
    return {'ok': 'success'}

if __name__ == '__main__':
    handler = service.create_handler(process)
    handler.start()
```

5. Start REST API:
```
uvicorn 'my_service:create_app'
```

6. Start task handler:
```
python my_service.py
```
