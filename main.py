from flask import Flask, render_template, request, redirect, send_file
from extractors.wwr import extract_wwr_jobs
from extractors.berlin import extract_berlin_jobs
from extractors.web3 import extract_web3_jobs
from file import save_to_file

app = Flask("NLess JOB")


"""
Do this when scraping a website to avoid getting blocked.

headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'Accept':
      'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
}

response = requests.get(URL, headers=headers)
"""


@app.route("/")
def home():
    return render_template("home.html")

db = {}

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        wwr = extract_wwr_jobs(keyword)
        berlin = extract_berlin_jobs(keyword)
        web3 = extract_web3_jobs(keyword)
        jobs = wwr + berlin + web3
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)
    
if __name__ == "__main__":
    app.run("0.0.0.0")
