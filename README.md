Below is the `README.md` tailored for your `Learn4Free` module, as requested. It reflects the current state of your project, including the name change and the acknowledgment for CourseKingdom.


## Learn4Free

A Python module to scrape free course information from coursekingdom.xyz.

## Features

- Scrape all courses or search for specific courses based on a search term
- Extracts course details including title, role, image, link, course link, coupon code, page number, and cleanly formatted date
- Utilizes multithreading for efficient scraping
- Includes a command-line interface for easy usage

## Installation

Install the package via pip:

```bash
pip install learn4free
```

## Usage

### As a Module

Import and use the `CourseScraper` class in your Python code:

```python
from learn4free import CourseScraper

# Initialize the scraper with optional search term and max workers
scraper = CourseScraper(max_workers=10, search_term="python")

# Scrape all courses
courses = scraper.scrape_all_courses()

# Process the courses
for course in courses:
    print(course)
```

### As a Command-Line Tool

Run the scraper from the command line after installation:

```bash
learn4free --help

learn4free --search "python" --page 2 --thread 10 --output courses.json
```

- If `--search` is provided, it scrapes courses matching the search term.


Example output:
```
                                                                        === Welcome to Learn4Free ===                                                                        
                                                            Scrape free courses from coursekingdom.xyz with ease!                                                            
                                                                --------------------------------------------                                                                 

Scraping Hacking on page 1 with 20 threads...

Scraping completed in 13.21 seconds
Total courses found: 12

                                                                               Scraped Courses                                                                               
╭───────┬───────┬───────────────────────────────────────────────┬─────────────────┬──────────────────────┬─────────────────┬────────────────────────────────────────────────╮
│  No.  │ Page  │ Title                                         │ Role            │ Coupon Code          │ Date            │ Course Link                                    │
├───────┼───────┼───────────────────────────────────────────────┼─────────────────┼──────────────────────┼─────────────────┼────────────────────────────────────────────────┤
│   1   │   1   │ Web Hacking For Beginners                     │ IT & Software   │ 5856A5B9D68A7AED1D84 │ 19 March, 2025  │ https://www.udemy.com/course/web-hacking-for-… │
├───────┼───────┼───────────────────────────────────────────────┼─────────────────┼──────────────────────┼─────────────────┼────────────────────────────────────────────────┤
│   2   │   1   │ BlackHat Live : Hands-On Hacking, No Theory   │ IT & Software   │ B27EE3CD5826316928BE │ 14 March, 2025  │ https://www.udemy.com/course/blackhat-live-ha… │
├───────┼───────┼───────────────────────────────────────────────┼─────────────────┼──────────────────────┼─────────────────┼────────────────────────────────────────────────┤
│   3   │   1   │ Android Hacking & Security: Ethical Hacking   │ IT & Software   │ FIRST1000            │ 12 March, 2025  │ https://www.udemy.com/course/android-hacking-… │
│       │       │ for Beginners                                 │                 │                      │                 │                                                │
├───────┼───────┼───────────────────────────────────────────────┼─────────────────┼──────────────────────┼─────────────────┼────────────────────────────────────────────────┤
│   4   │   1   │ Web Hacking For Beginners                     │ IT & Software   │ B0387F32AEAE39E22C78 │ 11 March, 2025  │ https://www.udemy.com/course/web-hacking-for-… │
├───────┼───────┼───────────────────────────────────────────────┼─────────────────┼──────────────────────┼─────────────────┼────────────────────────────────────────────────┤
│   5   │   1   │ Web Hacking For Beginners                     │ IT & Software   │ LEARNMARCH           │ 1 March, 2025   │ https://www.udemy.com/course/web-hacking-for-… │
├───────┼───────┼───────────────────────────────────────────────┼─────────────────┼──────────────────────┼─────────────────┼────────────────────────────────────────────────┤
│   6   │   1   │ Web Hacking For Beginners                     │ IT & Software   │ 150D60554FF786EB4CB5 │ 12 February,    │ https://www.udemy.com/course/web-hacking-for-… │
│       │       │                                               │                 │                      │ 2025            │                                                │
├───────┼───────┼───────────────────────────────────────────────┼─────────────────┼──────────────────────┼─────────────────┼────────────────────────────────────────────────┤
│   7   │   1   │ Web Hacking For Beginners                     │ IT & Software   │ D7D06321E9E4047C4B03 │ 6 February,     │ https://www.udemy.com/course/web-hacking-for-… │
│       │       │                                               │                 │                      │ 2025            │                                                │
├───────┼───────┼───────────────────────────────────────────────┼─────────────────┼──────────────────────┼─────────────────┼────────────────────────────────────────────────┤
│   8   │   1   │ Web Hacking For Beginners                     │ IT & Software   │ 2155D715514885027251 │ 3 February,     │ https://www.udemy.com/course/web-hacking-for-… │
│       │       │                                               │                 │                      │ 2025            │                                                │
├───────┼───────┼───────────────────────────────────────────────┼─────────────────┼──────────────────────┼─────────────────┼────────────────────────────────────────────────┤
│   9   │   1   │ Web Hacking For Beginners                     │ IT & Software   │ 3E61ADB8E7C6E545E312 │ 19 January,     │ https://www.udemy.com/course/web-hacking-for-… │
│       │       │                                               │                 │                      │ 2025            │                                                │
├───────┼───────┼───────────────────────────────────────────────┼─────────────────┼──────────────────────┼─────────────────┼────────────────────────────────────────────────┤
│  10   │   1   │ Web Hacking For Beginners                     │ IT & Software   │ LEARN-JAN            │ 8 January, 2025 │ https://www.udemy.com/course/web-hacking-for-… │
├───────┼───────┼───────────────────────────────────────────────┼─────────────────┼──────────────────────┼─────────────────┼────────────────────────────────────────────────┤
│  11   │   1   │ Web Hacking For Beginners                     │ IT & Software   │ 6C8F88528D7DA2180A47 │ 2 January, 2025 │ https://www.udemy.com/course/web-hacking-for-… │
├───────┼───────┼───────────────────────────────────────────────┼─────────────────┼──────────────────────┼─────────────────┼────────────────────────────────────────────────┤
│  12   │   1   │ Web Hacking For Beginners                     │ IT & Software   │ DEC-LEARN-MORE       │ 27 December,    │ https://www.udemy.com/course/web-hacking-for-… │
│       │       │                                               │                 │                      │ 2024            │                                                │
╰───────┴───────┴───────────────────────────────────────────────┴─────────────────┴──────────────────────┴─────────────────┴────────────────────────────────────────────────╯
                                                                                                                                                                             
                                                                   === Thank you for using Learn4Free! ===                                                                   

```

## Requirements

- Python 3.6 or higher
- `requests`
- `beautifulsoup4`
- `fake-useragent`
- `rich`
## Notes

- **Website Dependency**: This scraper is tailored to the current structure of coursekingdom.xyz. Changes to the website may require updates to the code.
- **Responsible Use**: Respect the website’s terms of service. Adjust `max_workers` (default 20 in CLI, 30 in class) to avoid overloading the server.
- **Date Formatting**: Dates are cleaned to remove non-breaking spaces and extra whitespace for consistency.
- **Robustness**: Includes retry logic with exponential backoff for failed requests.

## Acknowledgments

A special thanks to [CourseKingdom](https://coursekingdom.xyz) for providing a platform to discover free courses, making education accessible to everyone!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.