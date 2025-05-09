# Job Scraper

A tool for monitoring job listings websites for changes by periodically scraping them and recording differences. Currently tracks internship and early career opportunities in Singapore from major tech and finance companies.

## Features

- Automatically scrapes job listing websites using Selenium with headless Chrome
- Extracts meaningful text content while ignoring styling, scripts, and tracking data
- Records changes in a chronological log with the newest entries at the top
- Uses BeautifulSoup for reliable HTML parsing
- Converts HTML to plain text to make changes easier to spot
- Currently tracks internship opportunities from:
  - Optiver
  - Stripe
  - Google
  - Jane Street
  - Hudson River Trading
  - Meta
  - Apple
  - Squarepoint Capital
  - Citadel
  - Open Government Products
  - Morgan Stanley
  - JPMorgan

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd JustApply
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install selenium beautifulsoup4 webdriver-manager
   ```

## Configuration

Edit the `daily_scraper.py` file to customize:

1. **URLs to monitor**: Modify the `urls` list in the `main()` function with the job sites you want to track. Each URL should be a direct link to the job listings page.

2. **Selenium settings**: The `setup_selenium()` function configures Selenium with headless Chrome. You can adjust Chrome options as needed.

3. **Wait time**: If websites need more time to load, you can adjust the `time.sleep()` value in the `fetch_page()` function (currently set to 5 seconds).

## Usage

### Manual Run

Run the script locally to check for changes:

```
python daily_scraper.py
```

The script will:
1. Load each configured URL using a headless Chrome browser
2. Wait for the page to fully load (including JavaScript)
3. Extract the text content of the page, removing all HTML markup, scripts, and styling
4. Compare it with the previously saved version (if any)
5. Record any changes in the `changes.md` file with a timestamp

### Automated Daily Checks

The repository includes a GitHub Actions workflow that automatically runs the scraper daily. The workflow:

1. Runs every day at 07:00 UTC (`cron: "0 7 * * *"`)
2. Can also be triggered manually using the "Run workflow" button
3. Sets up Python 3.11 and installs required dependencies
4. Runs the scraper script
5. Commits and pushes any changes to the repository

To enable automated checks:
1. Fork this repository
2. Go to the "Actions" tab
3. Enable GitHub Actions for your fork
4. The workflow will automatically run daily

The workflow will:
- Create a new commit with any detected changes
- Update the `changes.md` file with new diffs
- Update the `text_storage` directory with new content
- Commit message format: "🔄 Daily scrape update: YYYY-MM-DD HH:MM:SS UTC"

### First Run Behavior

**Important**: The first time you run the script for a URL, it will save the current content but won't show any meaningful changes (as there's nothing to compare against). The script will report:

```
Changes detected for [URL]
No previous version found
```

This is expected behavior. The script needs to establish a baseline before it can detect changes. For new job sites you add:

1. Run the script once to capture the initial state
2. Visit the site manually to check current listings
3. Run the script again on subsequent days to detect changes

The real value comes from running the script regularly (e.g., daily) after the initial run, as it will then show you exactly what changed on the job listings page since the last check.

## Output

Changes are recorded in `changes.md` in reverse chronological order (newest at top). For each run, the file shows:

- A timestamp for when the check was performed
- Status for each URL (changes detected or no changes)
- For changed pages, a diff showing what content was added/removed

Example:
```markdown
## 2023-09-15 10:30:45

### [https://example.com/jobs](https://example.com/jobs)

**Changes detected!**

```diff
--- old.txt
+++ new.txt
@@ -1,3 +1,4 @@
 Software Engineer
 Remote
+Machine Learning Engineer
 San Francisco
```

## Advanced Usage

### Adding New Sites

To add a new job site to monitor, add its URL to the `urls` list in the `main()` function:

```python
urls = [
    "https://existing-url.com/jobs",
    "https://new-site.com/careers"  # Add your new site here
]
```

### Customizing Text Extraction

The `extract_text()` function uses BeautifulSoup to:
1. Remove all script and style tags
2. Extract text content with line breaks between blocks
3. Normalize whitespace and remove empty lines

You can modify this function if certain sites require special handling.

## Troubleshooting

- **ChromeDriver issues**: The script uses webdriver-manager to automatically download the correct ChromeDriver version. If you encounter issues, try running with the `--headless` option removed to see the browser in action.

- **Website blocking**: Some websites may block automated access. Consider adding more realistic user agent strings or other headers as needed.

- **Long load times**: If the page content is not fully loaded before capturing, increase the `time.sleep()` value in the `fetch_page()` function.

- **Storage**: The script stores text content in the `text_storage` directory, with one file per URL. Each file contains only the extracted text content, making it easy to track changes over time.

- **GitHub Actions**: If the workflow fails, check the Actions tab for error messages. Common issues include:
  - Rate limiting from job sites
  - Changes in website structure
  - Network connectivity issues