from requests import get
from bs4 import BeautifulSoup

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    response = get(f"{base_url}{keyword}", headers=headers)
    if response.status_code != 200:
        print("Can't request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all('section', class_="jobs")
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]
                link = anchor['href']
                company, kind, region = anchor.find_all('span',
                                                        class_="company")
                title = anchor.find('span', class_='title')
                job_data = {
                    'link': f"https://weworkremotely.com{link}",
                    'company': company.string.replace(",", " "),
                    'location': region.string.replace(",", " "),
                    'position': title.string.replace(",", " ")
                }
                results.append(job_data)
        return results
