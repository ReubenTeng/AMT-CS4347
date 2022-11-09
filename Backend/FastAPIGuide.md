**Starting the server**

Step 1: Install all the required packages with

```$ pip install -r requirements.txt```

Step 2: Run the server with

```$ uvicorn main:app --reload```

Step 3: Go to http://localhost:80/docs to view the APIs

**Writing API functions**

Basic tutorial: https://fastapi.tiangolo.com/tutorial/

```
@app.{get/post/put/patch/delete}
def function_name(function_parameters):
    ***Logic for API***
    return result
```