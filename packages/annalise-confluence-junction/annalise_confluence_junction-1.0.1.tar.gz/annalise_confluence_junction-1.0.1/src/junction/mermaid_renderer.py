import os
import re
from typing import List
import uuid
from pyppeteer import executablePath, launch
import cairosvg
class MermaidRenderer():
    def __init__(self) -> None:
        html_file = open('./index.html')
        self.html = html_file.read()


    async def render_mermaid_svg(self,file_name:str,diagram:List[str])->str:
        diagram_content = '\n'.join(diagram)
        html = re.sub(r'MERMAID', diagram_content, self.html)
        browser = await launch(executablePath='/usr/bin/chromium',args=['--no-sandbox'])
        page = await browser.newPage()
        diagram_name = f'{uuid.uuid4()}.png'
        await page.setContent(html)
        await page.waitForSelector('svg')
        svg =  await page.evaluate("() => document.querySelector('svg').outerHTML")
        os.makedirs(f'mermaid/{file_name}', exist_ok=True)
        cairosvg.svg2png(bytes(svg,'utf-8'),write_to=f'mermaid/{file_name}/{diagram_name}')
        await browser.close()
        return diagram_name