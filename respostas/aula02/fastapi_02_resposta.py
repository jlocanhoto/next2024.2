"""Objetivo:

Exemplo prático de uma resposta HTML pura ao invés de um objeto JSON."""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/', response_class=HTMLResponse)
async def read_root():
    html_page = """
    <html>
        <head>
            <title>NExT 2025</title>
        </head>
        <body>
            <div style="display: flex; flex-direction: column; align-items: center">
                <img src="https://www.cesar.school/wp-content/themes/alfama/assets/img/marca.svg" />
                <h1>Desenvolvimento Web</h1>
                <h2 style="color: blue">Módulo 07</h2>
            </div>
        </body>
    </html>"""

    return html_page
