# From @TonyCrane's hooks, adapted for tikz-qtree support

import logging
import os
import re

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from utils.markdown_utils import (
    get_indentation_level,
    replace_indented_block_start_with_options,
)
from utils.tikz_renderer import TikZQtreeRenderer

enabled = os.getenv("TIKZ_QTREE", "1") == "1" or os.getenv("FULL", "0") == "true"
logger = logging.getLogger("mkdocs.hooks.tikzqtree")

if enabled:
    logger.info("hook - tikzqtree is loaded and enabled")
else:
    logger.info("hook - tikzqtree is disabled")

CACHE = False


def on_page_markdown(
    markdown: str, page: Page, config: MkDocsConfig, files: Files, **kwargs
) -> str:
    if not enabled:
        return markdown

    def _replace_qtree(matched: re.Match) -> str:
        options = matched.group("options")
        contents = matched.group("contents")
        zoom = matched.group("zoom")
        first_line_indentation_level = get_indentation_level(contents)

        contents_lines = [line for line in contents.splitlines()]
        contents_remain = []

        for idx, line in enumerate(contents_lines):
            if get_indentation_level(line) < first_line_indentation_level:
                contents_remain = contents_lines[idx:]
                contents_lines = contents_lines[:idx]
                break

        contents_clean = "\n".join(contents_lines)
        renderer = TikZQtreeRenderer(options, contents_clean)
        svg_str = "".join(
            renderer.write_to_svg(CACHE)
            .replace("<?xml version='1.0' encoding='UTF-8'?>", "")
            .splitlines()
        )

        svg_str = svg_str.replace('stroke="#000"', 'stroke="currentColor"')
        svg_str = svg_str.replace("stroke='#000'", "stroke='currentColor'")
        svg_str = svg_str.replace("stroke='none'", "stroke='currentColor'")
        svg_str = svg_str.replace('stroke="none"', 'stroke="currentColor"')

        svg_str = svg_str.replace('fill="#000"', 'fill="currentColor"')
        svg_str = svg_str.replace("fill='#000'", "fill='currentColor'")

        return (
            matched.group("leading")
            + f'<div style="text-align: center; zoom: {zoom if zoom else "1.3"};">{svg_str}</div>'
            + "\n"
            + "\n".join(contents_remain)
        )

    markdown = replace_indented_block_start_with_options(
        r"(?<!\\)\\qtree", _replace_qtree, markdown
    )
    markdown = re.sub(r"\\\\qtree", r"\\qtree", markdown)

    return markdown
