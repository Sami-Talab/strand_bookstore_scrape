
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import csv
import re

def setup_selenium():
    # set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # run Chrome in headless mode
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    # specify the path to chromedriver in the project folder
    chromedriver_path = os.path.join(os.getcwd(), 'chromedriver')  
    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError(f"chromedriver not found at {chromedriver_path}. Please ensure it's in the project directory.")
    
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_section_books(section_url, option):
    # set up Selenium WebDriver
    driver = setup_selenium()

    page_number = 1
    more_pages = True
    all_books = []  # This will store all books across pages

    try:
        while more_pages:
            # Load the section page with the current page number
            paginated_url = section_url.format(page_number=page_number)
            driver.get(paginated_url)
            time.sleep(5)  # Wait for the page to load fully

            # Parse page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find all book containers
            book_containers = soup.find_all('div', class_='item-root-Chs text-center')

            # Check if the current page has no book containers
            if not book_containers:
                print(f"No more books found on page {page_number}.")
                break  # Stop if no more books are found

            # Extract book details
            books = []  # Temporary list to hold current page's books
            for container in book_containers:
                # Extract book title
                title_element = container.find('a', class_='item-name-LPg')
                title = title_element.get_text(strip=True) if title_element else 'Title not found'

                # Extract author
                author_element = container.find('li', class_='item-authorListItem-sxA')
                author = author_element.get_text(strip=True) if author_element else 'Author not found'

                # Extract price
                price_element = container.find('div', class_='item-price-RxI')
                price = ''.join([span.get_text(strip=True) for span in price_element.find_all('span')]) if price_element else 'Price not found'

                # Add book details to the list
                books.append({'Title': title, 'Author': author, 'Price': price})

            # Add the books from this page to the cumulative list
            all_books.extend(books)

            # Print out the books' information for the current page
            for book in books:
                print(f"Title: {book['Title']}")
                print(f"Author: {book['Author']}")
                print(f"Price: {book['Price']}")
                print('-' * 40)

            # Ask the user if they want to scrape more pages
            user_input = input(f"Do you want to scrape more pages? (current page: {page_number}) [y/n]: ").strip().lower()
            if user_input == 'n':
                more_pages = False
            else:
                page_number += 1  # Go to the next page

        # After all pages are scraped, ask the user if they want to save the data
        if all_books:  # Only ask to save if there are books to save
            save_data = input("Do you want to save the scraped data to a CSV file? [y/n]: ").strip().lower()
            if save_data == 'y':
                # Change location to where you want to save the file.
                csv_filename = f'/Users/samitalab/Downloads/{option}_books.csv'

                # Check if the file already exists to determine whether to append or write
                write_header = not os.path.exists(csv_filename)

                # Writing or appending the data to the CSV file
                with open(csv_filename, mode='a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['Title', 'Author', 'Price'])

                    # Write the header only if the file is new
                    if write_header:
                        writer.writeheader()
                        
                    # Write the book details
                    for book in all_books:
                        writer.writerow(book)

                print(f"Data saved to {csv_filename}")
            else:
                print("Data not saved.")
        else:
            print("No books to save.")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        driver.quit()

def get_book_isbn13(title):
    #URL for Google Books API
    base_url = "https://www.googleapis.com/books/v1/volumes"
    
    # parameters for the API request
    params = {
        # search for books with the given title
        'q': f'intitle:{title}',  
        'maxResults': 1  # limit to the first match
    }
    
    #Google APII request
    response = requests.get(base_url, params=params)
    
    #check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # check if there are any books in the response
        if 'items' in data and len(data['items']) > 0:
            book_info = data['items'][0]
            # extract ISBN-13 from the book's volumeInfo
            for identifier in book_info['volumeInfo'].get('industryIdentifiers', []):
                if identifier['type'] == 'ISBN_13':
                    return identifier['identifier']
        else:
            return None
    else:
        print(f"Error: Unable to connect to Google Books API. Status code: {response.status_code}")
        return None

def clean_title_for_url(title):
    #replace apostrophes followed by 's' with '-s'
    title = re.sub(r"'s", "-s", title)
    
    #remove standalone apostrophes
    title = re.sub(r"'", "", title)
    
    #remove special characters except hyphens and spaces, then replace spaces with hyphens
    title = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    title = re.sub(r'\s+', '-', title.strip())  
    
    return title.lower()

def find_and_scrape_book_details(title):
    # get ISBN-13 for the book title
    isbn13 = get_book_isbn13(title)
    
    #check if an ISBN-13 is found
    if not isbn13:
        print(f"No ISBN-13 found for '{title}'. Couldn't find the book.")
        return
    
    #clean the title to construct the URL
    cleaned_title = clean_title_for_url(title)

    #construct the Strand Books URL
    book_url = f'https://www.strandbooks.com/{cleaned_title}-{isbn13}.html'
    print(f"Trying URL: {book_url}")

    #send a GET request to check if the book URL exists
    response = requests.get(book_url)
    
    #check if the URL is accessible
    if response.status_code == 200:
        print(f"Book found! URL: {book_url}")
        
        # scrape the book details from the found URL using Selenium
        scrape_book_details_with_selenium(book_url)
    else:
        print(f"ISBN {isbn13} didn't work. Status code: {response.status_code}")
        print(f"Couldn't find the book '{title}' on Strand's website.")


def scrape_book_details_with_selenium(book_url):
    # set up Selenium WebDriver
    driver = setup_selenium()

    try:
        # fetch the book page
        driver.get(book_url)
        
        #rest period to fully load the JavaScript content
        time.sleep(10) 

        #parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # extract the book title
        title_element = soup.find('h1', class_='productFullDetail-productName-Qe1')
        title = title_element.find('div').get_text(strip=True) if title_element else 'Title not found'

        #extract the author
        author_element = soup.find('div', class_='productFullDetail-productAuthors-Ue2')
        author = author_element.find('div').get_text(strip=True).replace("By ", "") if author_element else 'Author not found'

        #extract the price
        price_element = soup.find('p', class_='productFullDetail-productPrice-pdI')
        price = ''.join([span.get_text(strip=True) for span in price_element.find_all('span')]) if price_element else 'Price not found'

        #print the extracted information
        print(f'Title: {title}')
        print(f'Author: {author}')
        print(f'Price: {price}')
        csv_filename = f'/Users/samitalab/Downloads/{title}_{author}_book_info.csv'
        # Save the extracted information to a CSV file
        with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Title', 'Author', 'Price'])
            
            # Write the header if the file is empty
            if file.tell() == 0:
                writer.writeheader()
                
            # Write the book details
            writer.writerow({'Title': title, 'Author': author, 'Price': price})
    


    except Exception as e:
        print(f"An error occurred while scraping: {e}")
    
    finally:
        #close the browser
        driver.quit()


def display_menu():
    menu_options = {
        1: 'comics',
        2: 'art',
        3: 'history',
        4: 'sports-and-games',
        5: 'science-technology-and-math',
        6: 'social-sciences',
        7: 'travel',
        8: 'world-languages',
        9: 'world-philosophy'
    }

    print("Menu:")
    for key, value in menu_options.items():
        print(f"{key}. {value}")

    try:
        choice = int(input("Enter the number of your choice: "))
        if choice in menu_options:
            print(f"You selected: {menu_options[choice]}")
            return menu_options[choice]
        else:
            print("Invalid choice. Please select a valid option.")
    except ValueError:
        print("Invalid input. Please enter a number.")

 
def menu_func():
    print("Hello User! Welcome to the Strand Book Shop Scraper\n")
   
    
    flag = True
    while flag:
        print("This system has two functionalities")
        print("1. Extract the details of a particular book you want")
        print("2. Scrape all the names and prices of books from a particular genre")
        print("3. Exit the program")
        choice = input("Please select which option you genre of books you want to scrape\n")
        if choice == "1":
            title = input("Enter the book title:").strip()
            find_and_scrape_book_details(title)
        elif choice == "2":
            option = display_menu()
            url= f"https://www.strandbooks.com/books-and-media/{option}.html?page={1}"

            scrape_section_books(url,option)
        elif choice == "3":
            print("GOODBYE")
            flag = False
        else:
            print("Invalid Option. Please select 1, 2 or 3")


if __name__ == "__main__":
    menu_func()
    