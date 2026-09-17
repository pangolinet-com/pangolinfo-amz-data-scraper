# Pangolinfo Amazon Data Scraper

**Author**: pangolinfo
**Version**: 0.0.1
**Type**: tool (e-commerce_data_extraction)

---

## Introduction

**Pangolinfo Amazon Data Scraper** empowers your AI agents with **high-fidelity** e-commerce intelligence. This official plugin transforms complex Amazon web pages into **clean, LLM-ready JSON**, seamlessly handling CAPTCHAs and enterprise-grade anti-bot systems in the background. With a **comprehensive suite of 7 specialized parsers**, it serves as the ultimate data foundation for building autonomous market research agents, real-time pricing monitors, and **E-commerce RAG workflows**.

**🎁 Welcome Bonus:** Start your AI journey with **60 complimentary credits**! New users receive free credits upon registration at the [Pangolinfo Portal](https://en.pangolinfo.com/), allowing you to test and deploy your first autonomous agents at **zero initial cost**.

## Features

**Comprehensive Amazon Coverage:** 7 specialized parsing engines tailored for every business logic—including Keywords, ASIN Details, BSR, New Releases, Categories, Storefronts, and Hijacker Tracking (Follow Sellers).

**Anti-Bot & CAPTCHA Bypass**: Enterprise-grade infrastructure featuring automated CAPTCHA solving and proxy rotation to ensure **uninterrupted, high-success** data retrieval.

**Global Marketplaces Support**: Seamlessly scrape data from regional Amazon domains (e.g., .com, .co.uk, .de, .co.jp).

**Real-Time Market Intelligence:** Instant access to live pricing, organic rankings, and BuyBox ownership status for immediate tactical decision-making.

**LLM-Ready Structured Data:** Transforms unstructured Amazon content into high-density, clean JSON. Optimized to minimize token consumption and maximize prompt accuracy for RAG and AI Agents.

**Granular Product Insights:** Extract deep-level specifications including bullet points, high-resolution imagery, SKU variations, and comprehensive review metrics.

## Setup

### Prerequisites

Before using this plugin, you need:

* A Pangolinfo account with sufficient API credits.
* A valid long-term API Key.
* Target Amazon URLs ready for scraping.

### Configuration Steps

1. **Get a Pangolinfo API Key**:

- Visit the [Pangolinfo Official Portal](https://en.pangolinfo.com/) and sign up.
- **Instant Reward:** Your account will be credited with **60 free units** upon registration—enough for roughly 60 deep ASIN scrapes or keyword searches.
- Obtain a **long-term valid API Key** through the [Authentication API](https://docs.pangolinfo.com/en-api-reference/authApi/auth?playground=open). *(Note: Do not use short-term tokens for Dify plugins to avoid expiration).*

2. **Configure the Plugin in Dify**:

- Navigate to the **Tools / Plugins** section in Dify.
- Select **Pangolinfo**.
- Click **To Authorize**.
- **API Key**: Enter your long-term Pangolinfo API key.
- Click "Save" to store the configuration globally.

### Usage

**1. Basic Keyword Search Extraction**

To extract organic rankings, prices, and sponsored ads from a search page:

**Parameters:**

**url**: https://www.amazon.com/s?k=wireless+mouse

**format**: json

**parserName**: amzKeyword

**bizContext**: {}

**2. Deep ASIN Detail Scraping**

To extract comprehensive details (bullet points, BuyBox, variations) of a specific product:

**Parameters:**

**url**: https://www.amazon.com/dp/B08H93ZRK9

**format**: json

**parserName**: amzProductDetail

**bizContext**: {}

**3. Niche Discovery (Best Sellers)**

To scrape the Top 100 products in a specific category:

**Parameters:**

**url**: https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/

**format**: json

**parserName**: amzBestSellers

**bizContext**: {}

**Understanding Parsers (parserName)**

You must select the correct parser that matches your provided url:

amzKeyword: Extracts product lists from search result URLs.

amzProductDetail: Extracts deep specs from standard product detail (/dp/ASIN) URLs.

amzBestSellers: Extracts Top 100 lists from Amazon BSR category URLs.

amzNewReleases: Extracts trending products from Amazon New Releases URLs.

amzProductOfCategory: Extracts macro product lists from Amazon category navigation URLs.

amzProductOfSeller: Extracts storefront listings from a specific Seller ID's URL.

amzFollowSeller: Monitors hijackers/competitors from the "Other Sellers on Amazon" URL of an ASIN.

**Output Format**

The plugin returns structured JSON data for the LLM to parse. Example output for amzKeyword:

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

## How It Works

1. **Job Initialization**: Your Dify Agent/Workflow constructs the target Amazon url and selects the parserName.
2. **Anti-Bot Processing**: Pangolinfo routes the request through residential proxies and bypasses Amazon's CAPTCHAs.
3. **HTML Parsing**: The raw HTML is fed into the specific algorithm (Parser) you selected.
4. **Data Structuring**: The unstructured HTML is converted into clean, LLM-ready JSON.
5. **Result Delivery**: The structured data is returned to your Dify application in real-time.

## Use Cases

1. **Automated Competitor Analysis (Workflow)**

Crawl a competitor's storefront to analyze their pricing strategy:

```plaintext
url: https://www.amazon.com/s?me=SELLER_ID_HERE
```

2. **Hijacker / BuyBox Monitoring (Agent)**

Set up an Agent to regularly check if unauthorized sellers are hijacking your product:

```plaintext
url: https://www.amazon.com
asin: YOUR_ASIN
```

3. **Blue Ocean Strategy Report (Workflow + Loop)**

Create a workflow that first calls amzBestSellers to get 10 hot ASINs, extracts their URLs, and uses a Loop Iteration node to call amzProductDetail on each to generate a comprehensive niche report.

## Best Practices

**Match URLs to Parsers Strictly**: Ensure the URL you provide structurally matches the parserName. Passing a product detail URL to a keyword parser will result in an error.

**Utilize Workflows for Scale**: Use Dify's Workflow Loop (Iteration) nodes for bulk ASIN processing instead of prompting an Agent to do it all at once.

**Prompt the LLM Properly**: In Agent apps, instruct the LLM explicitly: *"You must construct a valid Amazon URL (e.g., https://www.amazon.com/dp/ASIN) before calling the tool."*

**Use Long-Term Keys**: Always use an API key obtained via the Auth API to prevent sudden workflow failures due to token expiration.

## Performance Considerations

**Real-time Latency**: Since Pangolinfo fetches live data and solves CAPTCHAs on the fly, a single request may take anywhere from 3 to 15 seconds.

**Workflow Timeouts**: When looping through multiple URLs in a Dify Workflow, ensure you increase the overall node/app timeout settings to accommodate the combined processing time.

**Troubleshooting**

**Common Issues**

- **"Authentication Failed" error**:
  - Verify your API key is correctly entered.
  - Ensure you are using a long-term API key, not a temporary playground token.

- **"Invalid URL / Parsing Error"**:

  - Check if the url is a complete, accessible Amazon link (must include https://).
  - Verify that the parserName correctly corresponds to the type of page you are trying to scrape.

- **"Rate Limit Exceeded" / Insufficient Balance**:

  - Check your Pangolinfo account dashboard to ensure you have sufficient scraping credits.

- **Empty Data Returned**:

  - The specific Amazon page might be temporarily unavailable or out of stock. Try opening the URL manually in your browser.

- **API Limits**

  - Available credits are based on your Pangolinfo account plan.
  - All new accounts start with **60 free credits**. This allows you to explore the full potential of our 7-scenario parsers without a credit card.
  - Check your [account dashboard](https://tool.pangolinfo.com) on the Pangolinfo website for usage statistics.

## Security Considerations

* API keys are transmitted securely via HTTPS.
* Your specific search queries and target URLs are processed securely by Pangolinfo's enterprise servers.
* Ensure you do not expose your API key in public LLM chat logs.

**Privacy**

Please refer to the [Pangolinfo Privacy Policy](https://en.pangolinfo.com/legal/privacy) for information on how your data is handled when using this plugin.

## Support

- **Plugin Support**: Support@pangolinfo.com
- **API Documentation**: [Pangolinfo Scraper API Documentation](https://docs.pangolinfo.com/en-index)

**Official Website**: Visit [Pangolinfo](https://en.pangolinfo.com/)

## Additional Resources

* [Pangolinfo Scraper API Documentation](https://docs.pangolinfo.com/en-index)
* [Authentication API Guide](https://docs.pangolinfo.com/en-index#request-url)

*Last updated: March 2026*
