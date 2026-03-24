# Pangolinfo Amazon Scraper 插件使用说明

**作者**: pangolinfo
**版本**: 0.0.1
**类型**: tool (电商数据提取)

---

## 简介 (Introduction)

本插件集成了 Pangolinfo 强大的网页抓取与数据提取 API 服务，专为亚马逊 (Amazon) 数据场景量身定制。它能够在底层自动处理验证码、绕过复杂的反爬虫系统，并从杂乱的亚马逊网页中提取出干净、结构化的 JSON 数据。插件内置了 7 种专用的场景解析器，非常适合在 Dify 等 AI 应用中构建自主的市场调研智能体 (Agent)、监控竞品定价，或提取结构化的电商商业情报。

**🎁 新人福利：** 注册即领 **60个免费积分**！新用户在 [Pangolinfo 官网](https://www.pangolinfo.com) 注册后即可自动获得，支持您在**零成本**下开启并部署首个AI agent。

## 核心功能 (Features)

**全场景覆盖**: 内置 7 大专用解析器，全面支持关键词搜索、商品详情、BSR 热销榜、新品榜、类目列表、卖家店铺以及跟卖追踪。

**反爬与验证码绕过**: 依托企业级基础设施，确保高并发抓取成功率，无惧封控。

**全球站点支持**: 无缝抓取各个国家/地区的亚马逊站点数据（如 .com, .co.uk, .de, .co.jp 等）。

**实时数据提取**: 瞬间获取最新、最实时的商品定价、搜索排名和 BuyBox 购物车状态。

**纯净 JSON 输出**: 将非结构化的亚马逊 HTML 网页转换为高度结构化、完美适配大模型 (LLM) 解析的 JSON 格式。

**深度商品情报**: 能够提取包含五点描述、高清图片、变体列表和评论数等极高颗粒度的细节数据。

## 初始设置 (Setup)

### 准备工作

在使用本插件前，您需要准备：

* 一个有充足 API 请求额度的 Pangolinfo 账户。
* 一个有效的、长期可用的 API Key。
* 准备好您需要抓取的亚马逊目标网页 URL。

### 配置步骤

1. **获取 Pangolinfo API Key**:

- 访问 [Pangolinfo 官网](https://www.pangolinfo.com/zh/) 并注册账户。
- 确保您的账户中有足够的余额。
- 请通过 [Authentication API](https://docs.pangolinfo.com/cn-api-reference/authApi/auth?playground=open) 获取一个**长期有效的 API Key**。*（注意：请勿使用供临时测试的短期 Token，以免在 Dify 工作流中由于 Token 过期导致中断）。*

2. **在 Dify 中配置插件**:

- 导航至 Dify 侧边栏的 **工具 (Tools) / 插件 (Plugins)** 模块。
- 选择 **Pangolinfo**。
- 点击 **去授权 (To Authorize)**。
- **API Key**: 填入您的长效 Pangolinfo API Key。
- 点击“保存”，完成全局配置。

### 基础用法 (Usage)

1. **基础关键词搜索抓取**

用于从搜索结果页提取自然排名、当前价格和赞助广告 (SP Ads)：

**配置参数:**

**url**: https://www.amazon.com/s?k=wireless+mouse

**format**: json

**parserName**: amzKeyword

**bizContext**: {}

2. **深度 ASIN 详情抓取**

用于提取某款特定商品的深度细节（五点描述、BuyBox、变体等）：

**配置参数:**

**url**: https://www.amazon.com/dp/B08H93ZRK9

**format**: json

**parserName**: amzProductDetail

**bizContext**: {}

3. **蓝海市场挖掘 (BSR 榜单)**

用于抓取特定亚马逊类目的 Top 100 热卖商品：

**配置参数:**

**url**: https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/

**format**: json

**parserName**: amzBestSellers

**bizContext**: {}

**参数详解 (Parameters Explained)**

**理解解析器 (parserName)**

您必须选择与传入 url 结构完全匹配的解析器名称：

amzKeyword: 提取搜索结果页 (Search Result) 的商品列表。

amzProductDetail: 提取标准商品详情页 (/dp/ASIN) 的深度规格。

amzBestSellers: 提取亚马逊 BSR 类目导航页的 Top 100 榜单。

amzNewReleases: 提取亚马逊新品榜单页的热门潜力商品。

amzProductOfCategory: 提取亚马逊特定分类导航树下的宏观商品列表。

amzProductOfSeller: 提取特定卖家 ID (Seller ID) 店铺页的在售商品列表。

amzFollowSeller: 从 ASIN 的“其他卖家”报价页提取跟卖者/劫持者监控数据。

**输出格式 (Output Format)**

插件将返回结构化的 JSON 数据供 LLM 消费。以 amzKeyword 为例的输出结构如下：

```json
{
    "code": 200,
    "msg": "success",
    "data": {
        "keyword": "wireless mouse",
        "products": [
            {
                "asin": "B08H93ZRK9",
                "title": "Logitech Advanced Wireless Mouse...",
                "price": 29.99,
                "rating": 4.6,
                "review_count": 12450,
                "is_sponsored": false,
                "url": "https://www.amazon.com/dp/B08H93ZRK9"
            }
        ]
    }
}
```

## 工作原理 (How It Works)

1. **任务初始化**: 您在 Dify 的 Agent 或 Workflow 中构造出目标亚马逊 url 并指定 parserName。
2. **反爬处理**: Pangolinfo 将请求路由至高速代理池，并在底层静默绕过亚马逊的验证码机制。
3. **HTML 解析**: 获取到的原始网页代码被送入您指定的专用解析算法中。
4. **数据结构化**: 将非结构化的杂乱 HTML 转化为干净的、适合 LLM 语境的 JSON 格式。
5. **结果返回**: 结构化数据实时返回到您的 Dify 应用流程中。

**典型用例 (Use Cases)**

1. **自动化竞品店铺分析 (工作流 Workflow)**

抓取竞争对手的店铺主页，分析其全盘定价策略：

```plaintext
url: https://www.amazon.com/s?me=SELLER_ID_HERE
```

2. **跟卖与购物车监控 (智能体 Agent)**

设置一个定期执行的 Agent，监控是否有未经授权的卖家劫持了您的商品：

```plaintext
url: https://www.amazon.com
asin: YOUR_ASIN
```

3. **蓝海选品策略报告 (工作流 + 循环节点)**

构建一个高阶工作流：首先调用 amzBestSellers 获取前 10 名的热卖 ASIN，通过代码节点提取它们的详情页 URL，然后使用**循环节点 (Iteration)** 逐一调用 amzProductDetail 抓取深度细节，最终汇交给 LLM 生成全面的蓝海选品报告。

## 最佳实践 (Best Practices)

**严格匹配 URL 与解析器**: 确保您提供的 URL 结构与 parserName 完全对应。将商品详情页的 URL 传递给关键词解析器会导致请求错误。

**利用工作流处理批量任务**: 对于大量 ASIN 的数据抓取，请使用 Dify 工作流中的“循环节点”进行批量调度，而不是仅靠提示词让 Agent 一次性处理。

**正确书写 LLM 提示词**: 在 Agent 应用中，应明确指示 LLM：*“在调用工具前，你必须先自行拼装出合法的亚马逊网页 URL（例如：https://www.amazon.com/dp/ASIN ）。”*

**使用长效 Key**: 始终使用通过 Auth API 获取的长效 API Key，避免鉴权突然失效。

## 性能注意事项 (Performance Considerations)

**实时延迟**: 由于 Pangolinfo 是实时去目标网站抓取并解决验证码的，单次请求可能需要 3 到 15 秒不等的时间。

**工作流超时设置**: 当您在 Dify 工作流中利用循环节点批量处理多个 URL 时，整体耗时会叠加。请务必在 Dify 中调大节点的总体超时等待时间。

## 常见问题与故障排除 (Troubleshooting)**

### 常见错误排查

- **"Authentication Failed" (鉴权失败)**:

  - 验证您的 API Key 是否输入正确且未包含多余空格。
  - 确保您使用的是正式的长期 API Key，而不是仅供测试用的 Playground Token。

- **"Invalid URL / Parsing Error" (无效链接或解析错误)**:

  - 检查 url 是否为完整、可访问的亚马逊链接（必须以 https:// 开头）。
  - 核实 parserName 是否与该网页的实际类型完全相符。

- **"Rate Limit Exceeded" (余额/额度不足)**:

  - 登录您的 Pangolinfo 账户后台，检查剩余的点数和抓取额度是否充足。

- **返回数据为空**:

  - 特定商品或页面可能已下架/暂时无法访问。建议先在浏览器中手动打开该 URL 确认网页状态。

- **API 限制 (API Limits)**

  - 可用额度取决于您的 Pangolinfo 账户套餐。
  - 所有新账户均享有 **60个免费积分**。无需绑定信用卡，即可全面体验 7 大场景解析器的强大功能。
  - 请访问 Pangolinfo 网站查看您的[仪表盘](https://tool.pangolinfo.com/)，了解使用统计信息。

## 安全与隐私 (Security & Privacy)

* API Key 和数据传输全程使用安全的 HTTPS 加密协议。
* 您特定的搜索查询和目标 URL 均由 Pangolinfo 企业级服务器安全处理。
* 请注意不要在公开的 LLM 聊天日志或公开应用中明文暴露您的 API Key。
* 关于您的数据将如何被处理，请参阅 [Pangolinfo 隐私政策](https://www.pangolinfo.com/zh/privacy-policy-cn/)。

## 支持与联系方式 (Support)

如遇任何技术问题或需要定制化解析需求，请联系我们：

* **邮箱支持**: Support@pangolinfo.com
* **官方网站**: [https://www.pangolinfo.com](https://www.pangolinfo.com/zh/)

## 附加资源 (Additional Resources)

* [Pangolinfo 官方 API 文档](https://docs.pangolinfo.com/cn-index)
* [API 鉴权与获取指南](https://docs.pangolinfo.com/cn-index#%E8%AF%B7%E6%B1%82url)

*最后更新：2026年3月*
