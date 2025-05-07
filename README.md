# Job Scraper

A tool for monitoring job listings websites for changes by periodically scraping them and recording differences.

## Features

- Automatically scrapes job listing websites using Selenium with headless Chrome
- Extracts meaningful text content while ignoring styling, scripts, and tracking data
- Records changes in a chronological log with the newest entries at the top
- Uses BeautifulSoup for reliable HTML parsing
- Converts HTML to plain text to make changes easier to spot

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

Edit the `job_scraper.py` file to customize:

1. **URLs to monitor**: Modify the `urls` list in the `main()` function with the job sites you want to track.

2. **Selenium settings**: The `setup_selenium()` function configures Selenium with headless Chrome. You can adjust Chrome options as needed.

3. **Wait time**: If websites need more time to load, you can adjust the `time.sleep()` value in the `fetch_page()` function.

## Usage

Run the script to check for changes:

```
python job_scraper.py
```

The script will:
1. Load each configured URL using a headless Chrome browser
2. Wait for the page to fully load (including JavaScript)
3. Extract the text content of the page
4. Compare it with the previously saved version (if any)
5. Record any changes in the `changes.md` file with a timestamp

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
--- old.html
+++ new.html
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

If certain sites require special handling, you can modify the `extract_text()` function to adjust how text is extracted from HTML.

## Troubleshooting

- **ChromeDriver issues**: The script uses webdriver-manager to automatically download the correct ChromeDriver version. If you encounter issues, try running with the `--headless` option removed to see the browser in action.

- **Website blocking**: Some websites may block automated access. Consider adding more realistic user agent strings or other headers as needed.

- **Long load times**: Increase the `time.sleep()` value if the page content is not fully loaded before capturing.