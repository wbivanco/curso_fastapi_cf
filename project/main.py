from fastapi import FastAPI

app = FastAPI(
    title='Proyecto para reseñar películas',
    description='En este proyecto seremos capaces de reseñar películas.',
    version='1'
)

@app.on_event('startup')
def starup():
    print('El servidor va a empezar.')

@app.on_event('shutdown')
def shutdown():
    print('El servidor se encuentra finalizando.')

@app.get('/')
async def index():
    return 'Hola mundo, desde un servidor en FastAPI'

@app.get('/about')
async def about():
    return 'About'