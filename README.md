Here is the updated `README.md` file, including a note about changing the CSV file path:

```markdown
# Strand Book Shop Scraper

This Python project is designed to scrape book details from the Strand Book Shop website. The scraper can extract details of a particular book or scrape an entire section of books by genre. The data includes the book's title, author, and price, and can be saved to a CSV file.

## Purpose

The scraper aims to help book enthusiasts, researchers, or developers quickly gather information about books available in specific genres from the Strand Book Shop. The scraper automates the process of collecting data, making it easier to analyze pricing trends, popular authors, and available genres without manually browsing through the website.

## Website Chosen

The website used is [Strand Book Shop](https://www.strandbooks.com), a well-known independent bookstore. It was chosen for its vast collection of books across various genres and the fact that its structured layout allows for easy scraping using Python libraries like Selenium and BeautifulSoup.

## Features

1. **Single Book Search:** Given the title of a book, the scraper will attempt to retrieve its ISBN-13 number via the Google Books API and search the Strand website to fetch its details (title, author, and price).
2. **Genre-based Scraping:** You can select a genre from the menu, and the scraper will loop through the genre pages, collecting details about each book (title, author, and price).
3. **Data Export to CSV:** After scraping, you have the option to save the collected data to a CSV file for further analysis.

## How to Run

### Prerequisites

Before running the project, ensure you have the following installed:
- Python 3.x
- Chrome browser
- Chromedriver (for Selenium)

### Installation

1. **Clone the repository:**

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Setup

1. **Download and Set Up ChromeDriver:**

   Ensure you download the correct version of [ChromeDriver](https://sites.google.com/chromium.org/driver/downloads) for your operating system. Place the `chromedriver` executable in the root directory of the project.

2. **Run the Scraper:**

You can now run the scraper using the following command:

```bash
python <your-script-name>.py
```

### Usage

Upon running the script, you will be presented with two options:

1. **Extract details of a particular book:**  
   Enter the title of the book, and the scraper will find the book's details using its ISBN-13.

2. **Scrape books from a specific genre:**  
   Select a genre from the displayed menu, and the scraper will gather the titles, authors, and prices of books available in that genre.

You will have the option to save the scraped data into a CSV file for later use.

### Note on Saving Data

The scraper will prompt you to save the scraped data into a CSV file. **Make sure to update the file path to your desired location** before running the scraper. The default path is set in the script but should be adjusted to fit your system's folder structure.

### Example

Here’s how to scrape the *Art* section of the website:

1. Clone the repository and navigate to the project folder.
2. Run the script: 

```bash
python <your-script-name>.py
```

3. Choose the option to scrape a genre, then select the corresponding number for "Art" when prompted.
4. After scraping, you will be asked whether you'd like to save the results to a CSV file.

### Limitations

- **Headless Chrome Setup:** Ensure ChromeDriver is properly installed and configured for the scraper to work.
- **Dynamic Content:** The scraper waits for 5-10 seconds to ensure JavaScript-based content fully loads, but the timing may vary depending on internet speed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Google Books API](https://developers.google.com/books)
```
