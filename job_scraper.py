import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, urljoin
import os
from dotenv import load_dotenv
from datetime import datetime
from openai import OpenAI
from pydantic import BaseModel
from typing import List
import instructor

# Define our data models
class Job(BaseModel):
    title: str
    location: str
    link: str
    company: str

class JobList(BaseModel):
    jobs: List[Job]

class JobScraper:
    def __init__(self, url, client):
        print(f"🚀 Initializing JobScraper with URL: {url}")
        self.url = url
        self.domain = urlparse(url).netloc
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.client = instructor.from_openai(client)

    def fetch_page(self):
        print(f"🌐 Fetching page content from {self.url}")
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            print("Page fetched successfully")

            # Save raw HTML
            with open('raw_html.html', 'w', encoding='utf-8') as f:
                f.write(response.text)

            return response.text
        except requests.RequestException as e:
            return None

    def extract_jobs_with_gpt(self, html_content):
        if not html_content:
            return []

        # Clean the HTML to make it more manageable
        soup = BeautifulSoup(html_content, 'html.parser')
        # Remove scripts, styles, and other non-essential elements
        for script in soup(["script", "style", "meta", "link"]):
            script.decompose()
        clean_html = str(soup)

        # Save cleaned HTML
        with open('cleaned_html.html', 'w', encoding='utf-8') as f:
            f.write(clean_html)

        # Prepare the prompt for GPT-4
        prompt = f"""
        You are a helpful assistant that extracts job listings from HTML content. You will be given a chunk of HTML content that contains job listings.

        For each job listing, extract:
        1. Job title
        2. Location
        3. Application link (URL)
        4. Company name
        """

        try:
            job_list = self.client.chat.completions.create(
                model="gpt-4o-mini",
                response_model=JobList,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": clean_html}
                ]
            )
            print(f"Successfully extracted {len(job_list.jobs)} jobs")
            return job_list.jobs

        except Exception as e:
            return []

    def scrape(self):
        print("🔄 Starting job scraping process")
        html_content = self.fetch_page()
        if html_content:
            jobs = self.extract_jobs_with_gpt(html_content)
            print(f"Scraping completed. Found {len(jobs)} jobs")
            return jobs
        return []

def generate_markdown_table(jobs):
    print("Generating markdown table from job listings")
    if not jobs:
        print("No jobs found for markdown generation")
        return "No jobs found."

    # Group jobs by company
    jobs_by_company = {}
    for job in jobs:
        company = job.company
        if company not in jobs_by_company:
            jobs_by_company[company] = []
        jobs_by_company[company].append(job)

    markdown = ""
    for company, company_jobs in jobs_by_company.items():
        print(f"🏢 Processing jobs for company: {company}")
        markdown += f"## {company}\n\n"
        markdown += "| Title | Location | Link |\n"
        markdown += "|-------|----------|------|\n"

        for job in company_jobs:
            title = job.title
            location = job.location
            link = job.link

            markdown += f"| {title} | {location} | [Apply]({link}) |\n"

        markdown += "\n"

    return markdown

def main():
    load_dotenv()
    client = OpenAI()

    # List of URLs to scrape
    urls = [
        "https://optiver.com/working-at-optiver/career-opportunities/?_gl=1*x7c8ib*_up*MQ..*_ga*MTA5OTMxMjk3Mi4xNzQ1NjQxMDk2*_ga_YMLN3CLJVE*MTc0NTY0MTA5NS4xLjEuMTc0NTY0MTA5OC4wLjAuMA..&numberposts=10&paged=1&office=singapore&level=internship",
        "https://www.janestreet.com/join-jane-street/open-roles/?type=internship&location=singapore",
        "https://stripe.com/jobs/search?office_locations=Asia+Pacific--Singapore&tags=University",
        "https://www.google.com/about/careers/applications/jobs/results/?src=Online%2FGoogle%20Website%2FByF&utm_source=Online%20&utm_medium=careers_site%20&utm_campaign=ByF&distance=50&employment_type=INTERN&company=Fitbit&company=Google&location=Singapore",
    ]

    all_jobs = []
    for url in urls:
        print(f"\n🌐 Processing URL: {url}")
        scraper = JobScraper(url, client)
        jobs = scraper.scrape()
        all_jobs.extend(jobs)
        print(f"Found {len(jobs)} jobs from {url}")

    markdown_content = f"""# Job Listings

Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{generate_markdown_table(all_jobs)}

## Notes
- All job listings are scraped from their respective company career pages
- Please check the original job postings for the most up-to-date information
- Application links are provided for each position
"""

    # Save results to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"\nTotal jobs found: {len(all_jobs)}")
    print("💾 Results saved to README.md")

if __name__ == "__main__":
    main()