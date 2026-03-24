from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from tools.scrape_keyword import ScrapeKeywordTool


class PangolinProvider(ToolProvider):

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            for _ in ScrapeKeywordTool.from_credentials(credentials).invoke(
                tool_parameters={"url": "https://www.amazon.com"}
            ):
                pass
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
