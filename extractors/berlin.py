from requests import get
from bs4 import BeautifulSoup

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def extract_berlin_jobs(keyword):
    base_url = "https://berlinstartupjobs.com/skill-areas/"
    response = get(f"{base_url}{keyword}/", headers=headers)

    if response.status_code != 200:
        print("Can't request website")
        return []

    results = []
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("div", class_="bjs-jlid__wrapper")

    for job in jobs:
        title = job.find("h4", class_="bjs-jlid__h").find("a")
        company = job.find("a", class_="bjs-jlid__b").text
        description = job.find("div", class_="bjs-jlid__description").text.strip()
        url_link = title.get("href")

        job_data = {
            'link': url_link,
            'company': company.replace(",", " "),
            'location': "Unknown", 
            'position': title.text.replace(",", " "),
            'description': description.replace(",", " ")
        }
        results.append(job_data)

    return results