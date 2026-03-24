from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from schemas.scrape import ParserName, OutputFormat, ScrapeRequest, BizContext
from tools.scrape import Scraper


class ScrapeFollowSellersTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        request_dict = ScrapeRequest(
            url=tool_parameters["url"],
            format=OutputFormat.JSON,
            parserName=ParserName.AMZ_FOLLOW_SELLERS,
            bizContext=BizContext(asin=tool_parameters["asin"])
        ).model_dump(mode='json', by_alias=True)

        scraper = Scraper(
            api_key=self.runtime.credentials["api_key"]
        )

        result = scraper.scrape(uri="/api/v1/scrape/follow-seller", **request_dict)
        yield self.create_json_message(result)
