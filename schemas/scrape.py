from typing import Optional
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum


class OutputFormat(str, Enum):
    JSON = "json"
    HTML = "html"
    MARKDOWN = "markdown"


class ParserName(str, Enum):
    AMZ_KEYWORD = "amzKeyword"
    AMZ_PRODUCT_DETAIL = "amzProductDetail"
    AMZ_PRODUCT_CATEGORY = "amzProductOfCategory"
    AMZ_PRODUCT_SELLER = "amzProductOfSeller"
    AMZ_NEW_RELEASES = "amzNewReleases"
    AMZ_BEST_SELLERS = "amzBestSellers"
    AMZ_FOLLOW_SELLERS = "amzFollowSeller"


class BizContext(BaseModel):
    asin: Optional[str] = Field(
        None,
        description="ASIN 编号，可选",
        examples=["B08N5WRWNW"]
    )


class ScrapeRequest(BaseModel):
    url: HttpUrl = Field(
        ...,
        description="目标网页的完整URL",
        examples=["https://example.com"]
    )
    format: OutputFormat = Field(
        ...,
        description="数据输出格式, 可选项: json, html, markdown"
    )
    parser_name: ParserName = Field(
        ...,
        alias="parserName",
        description="HTML解析器名称"
    )
    bizContext: Optional[BizContext] = Field(
        None,
        description="业务上下文，可选"
    )
