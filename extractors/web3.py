from requests import get
from bs4 import BeautifulSoup

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def extract_web3_jobs(keyword):
    base_url = "https://web3.career/"
    response = get(f"{base_url}{keyword}-jobs", headers=headers)
    if response.status_code != 200:
        print("Can't request website")
        return []

    results = []
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all('tr', class_="table_row")
    for job in jobs:
        title_element = job.find("h2", class_="fs-6 fs-md-5 fw-bold my-primary")
        title = title_element.text.strip() if title_element else "Title not found"
        company_element = job.find("h3", style="color: white; font-size: 12px;")
        company = company_element.text.strip() if company_element else "Company not found"
        location = job.find("td", class_="job-location-mobile").text.strip()
        onclick_value = job.get('onclick', '')
        link = ''
        if onclick_value:
            link_part = onclick_value.split("'")
            if len(link_part) > 1:
                link = base_url + link_part[1].lstrip('/')
        job_data = {
            'position': title.replace(",", " "),
            'company': company.replace(",", " "),
            'location': location.replace(",", " "),
            'link': link
        }
        results.append(job_data)

    return results