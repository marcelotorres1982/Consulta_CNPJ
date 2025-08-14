# 🔍 CNPJ Lookup Tool

This project allows you to query public information of Brazilian companies (CNPJs), extracting phone numbers and emails directly from https://cnpj.biz using web scraping with Selenium, and displaying the results in a modern GUI built with CustomTkinter.

🚀 Features

Query CNPJs with or without punctuation (e.g., 00.000.000/0000-00 or 00000000000000)

    Automatic extraction of:
    Trade Name (Nome Fantasia)
    Phone number (href="tel:")
    Email (href="mailto:")
    Modern graphical interface with copy-friendly fields for phone and email
    Headless Selenium processing (browser runs in the background)

| Tool              | Purpose                                            |
| ----------------- | -------------------------------------------------- |
| **Python**        | Main programming language                          |
| **CustomTkinter** | Modern GUI based on Tkinter                        |
| **Selenium**      | Web automation and scraping                        |
| **BeautifulSoup** | HTML parsing and extraction                        |
| **re (Regex)**    | CNPJ character cleaning                            |
| **ChromeDriver**  | Automated browser (requires separate installation) |


Python 3.8+

Google Chrome installed

ChromeDriver compatible with your Chrome version

Install dependencies with:

pip install customtkinter selenium beautifulsoup4


⚙️ Usage

Clone the repository:

    git clone https://github.com/your-username/repository-name.git
    cd repository-name


Run the script:

    python script_name.py


Enter a valid CNPJ in the interface and click Search.

📌 Notes

The data source (cnpj.biz) is public, but the site does not provide an official API.

Scraping respects reasonable limits (~30 queries per day).

This project is intended for educational and personal use only.
