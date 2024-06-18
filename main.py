from blacksheep import Application, Request
from blacksheep.server.responses import html
import aiofiles
from typing import Dict

class TemplateCache:
    """
    A simple template cache for reading HTML templates asynchronously.
    """

    _cache: Dict[str, str]

    def __init__(self):
        """
        Initializes the TemplateCache.
        """
        self._cache = {}

    async def read_template(self, file_name: str) -> str:
        """
        Reads an HTML template from the file system asynchronously,
        caching it for subsequent reads.

        Args:
            file_name (str): The name of the HTML template file.

        Returns:
            str: The content of the HTML template.
        """
        if file_name not in self._cache:
            async with aiofiles.open(f"./templates/{file_name}", "r", encoding="utf-8") as file:
                self._cache[file_name] = await file.read()
        return self._cache[file_name]


app = Application()
cache = TemplateCache()

@app.router.get("/")
async def home(request: Request):
    return html(await cache.read_template("mainpage.html"))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8000)