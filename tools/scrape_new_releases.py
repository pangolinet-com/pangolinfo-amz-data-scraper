from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from schemas.scrape import ParserName, OutputFormat, ScrapeRequest
from tools.scrape import Scraper


class ScrapeNewReleasesTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        request_dict = ScrapeRequest(
            url=tool_parameters["url"],
            format=OutputFormat.JSON,
            parserName=ParserName.AMZ_NEW_RELEASES
        ).model_dump(mode='json', by_alias=True)

        scraper = Scraper(
            api_key=self.runtime.credentials["api_key"]
        )

        result = scraper.scrape(**request_dict)
        yield self.create_json_message(result)
