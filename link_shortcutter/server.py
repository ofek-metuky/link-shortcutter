import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from link_shortcutter import config
from link_shortcutter.db_wrapper import DbWrapper
from link_shortcutter.models import LinkItem

app = FastAPI()
templates = Jinja2Templates(directory=config.templates_path)


@app.get("/{short_name}")
def get_link(short_name: str):
    with DbWrapper() as db:
        links = list(db.get_links(short_name))
        if len(links) == 1:
            return RedirectResponse(links[0])

        return RedirectResponse(f"ui/view_links/{short_name}")


@app.post("/link/")
def add_link(link_item: LinkItem):
    with DbWrapper() as db:
        links = list(db.query_links(short_name=link_item.short_name))
        if not links:
            db.add_link(link_item)
            return

        raise HTTPException(status_code=400, detail="short name already exists")


@app.put("/link/")
def update_link(link_item: LinkItem):
    with DbWrapper() as db:
        db.update_link(link_item)


@app.delete("/link/{short_name}")
def delete_link(short_name: str):
    with DbWrapper() as db:
        db.delete_link(short_name)


@app.get("/ui/add_link", response_class=HTMLResponse)
def add_link_page(request: Request):
    return templates.TemplateResponse("add_link.j2", dict(request=request))


@app.get("/ui/edit_links/{short_name}", response_class=HTMLResponse)
def edit_link_page(request: Request, short_name: str):
    with DbWrapper() as db:
        links = list(db.query_links(short_name=short_name))
        if len(links) == 1:
            return templates.TemplateResponse("update_link.j2", dict(request=request, link_item=links[0]))

        return RedirectResponse(f"/ui/view_links/{short_name}")


@app.get("/ui/view_links/", response_class=HTMLResponse)
def view_all_links_page(request: Request):
    with DbWrapper() as db:
        link_items = list(db.get_all_links())
        return templates.TemplateResponse("view_all_links.j2", dict(request=request, link_items=link_items))


@app.get("/ui/view_links/{short_name}", response_class=HTMLResponse)
def view_links_page(request: Request, short_name: str):
    with DbWrapper() as db:
        links = list(db.get_similar_links(short_name))
        return templates.TemplateResponse("view_links.j2",
                                          dict(request=request, links=links, short_name=short_name))


if __name__ == '__main__':
    uvicorn.run("link_shortcutter.server:app", port=80, host="0.0.0.0")
