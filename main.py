from fastapi import FastAPI, Request

app = FastAPI() 

@app.get('/')
async def root():
    return {'message': 'hafflo'}

@app.get('/posts/')
def get_posts(data: Request):
    return {'data': data.query_params}