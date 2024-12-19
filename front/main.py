from datetime import date
from typing import Annotated
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent, PageEvent
from pydantic import BaseModel, Field, HttpUrl
from fastui.forms import FormFile, SelectSearchResponse, Textarea, fastui_form
import hashlib
import json
import time
import urllib.request
import requests
SERVER_POLL_TIME = 2
SERVER_STATUS_STREAM_ACTIVE = "dl"

app = FastAPI()


class InputForm(BaseModel):
    acestream_id: str = Field(title="Acestream PID")


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def users_table() -> list[AnyComponent]:
    """
    Show a table of four users, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Div(
                    components=[
                        c.Heading(text='Acestream Server', level=2),  # renders `<h2>Users</h2>`
                        c.ModelForm(model=InputForm, display_mode='default', submit_url="/api/send_pid"),
                        #c.Button(text='Load Content from Server', on_click=PageEvent(name='server-load')),
                    ]
                )
            ]
        )
    ]


def get_acestream_id_by_url(url):
    return requests.get(url, allow_redirects=False).headers.get("Location").removeprefix("acestream://")

def api_request(url):
    response = urllib.request.urlopen(url)
    return json.load(response).get("response", {})


def start_stream(server_hostname, server_port, stream_pid):
    stream_uid = hashlib.sha1(stream_pid.encode()).hexdigest()

    response = api_request(
        f"http://{server_hostname}:{server_port}/ace/getstream?format=json&sid={stream_uid}&id={stream_pid}"
    )

    return (response["stat_url"], response["playback_url"])

def await_playback(statistics_url):
    while True:
        response = api_request(statistics_url)

        if response.get("status") == SERVER_STATUS_STREAM_ACTIVE:
            print("Ready!\n")
            return True

        time.sleep(SERVER_POLL_TIME)

@app.post('/api/send_pid', response_model=FastUI, response_model_exclude_none=True)
async def login_form_post(form: Annotated[InputForm, fastui_form(InputForm)]):
    try:
        HttpUrl(form.acestream_id)
        pid = get_acestream_id_by_url(form.acestream_id)
    except:
        pid = form.acestream_id

    statistics_url, playback_url = start_stream(
        "server_acestream", 6878, pid
    )
    if not await_playback(statistics_url):
        return
    return [c.Paragraph(text=playback_url)]


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))