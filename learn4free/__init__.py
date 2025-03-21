from .scraper import CourseScraper
import argparse
import time
import json
from rich.console import Console
from rich.table import Table
from rich import box

# Initialize rich console
console = Console()

def print_welcome():
    """Print a welcome message using rich."""
    console.print("[bold cyan]=== Welcome to Learn4Free ===[/]", justify="center")
    console.print("[green]Scrape free courses from coursekingdom.xyz with ease![/]", justify="center")
    console.print("[yellow]--------------------------------------------[/]", justify="center")
    console.print()

def create_table(courses):
    """Create a rich table for displaying courses with full links."""
    table = Table(title="[bold magenta]Scraped Courses[/]", box=box.ROUNDED, show_lines=True)
    table.add_column("No.", style="cyan", justify="center", width=5)
    table.add_column("Page", style="cyan", justify="center", width=5)
    table.add_column("Title", style="blue", no_wrap=False)
    table.add_column("Role", style="blue", width=15)
    table.add_column("Coupon Code", style="green", no_wrap=False)  # Full coupon code
    table.add_column("Date", style="yellow", width=15)
    table.add_column("Course Link", style="blue", no_wrap=False)  # Full course link

    for i, course in enumerate(courses, 1):
        table.add_row(
            str(i),
            str(course['page']),
            course['title'] or 'N/A',
            course['role'] or 'N/A',
            course['coupon_code'] or 'N/A',
            course['date'] or 'N/A',
            course['course_link'] or 'N/A'
        )
    return table

def save_to_file(courses, output_file):
    """Save courses to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=4, ensure_ascii=False)
    console.print(f"[green]Results saved to {output_file}[/]")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Scrape courses from coursekingdom.xyz with Learn4Free")
    parser.add_argument('--search', type=str, help="Search term for courses (required if --page not provided)")
    parser.add_argument('--page', '-p', type=int, help="Specific page to scrape (required if --search not provided)")
    parser.add_argument('--thread', '-t', type=int, default=20, help="Number of threads (default: 20)")
    parser.add_argument('--output', '-o', type=str, help="Output file to save results (e.g., courses.json)")
    args = parser.parse_args()

    # Require either --search or --page
    if not args.search and not args.page:
        parser.error("At least one of --search or --page/-p is required to prevent scraping all courses.")

    # Print welcome message
    print_welcome()

    # Validate thread count
    max_workers = max(1, min(args.thread, 30))  # Cap between 1 and 30
    search_term = args.search if args.search else "all courses"
    action = f"Scraping {search_term}"
    if args.page:
        action += f" on page {args.page}"
    action += f" with {max_workers} thread{'s' if max_workers != 1 else ''}..."

    console.print(f"[green]{action}[/]")
    
    # Initialize the scraper
    scraper = CourseScraper(max_workers=max_workers, search_term=args.search)

    # Scrape with timing
    start_time = time.time()
    if args.page:
        # Scrape a specific page if --page is provided
        courses = scraper.scrape_page(args.page)
    elif args.search:
        # Scrape all pages for the search term if only --search is provided
        courses = scraper.scrape_all_courses()
    elapsed_time = time.time() - start_time

    # Display results
    console.print(f"\n[green]Scraping completed in {elapsed_time:.2f} seconds[/]")
    console.print(f"[green]Total courses found: {len(courses)}[/]\n")

    if courses:
        table = create_table(courses)
        console.print(table)
        if args.output:
            save_to_file(courses, args.output)
    else:
        console.print("[red]No courses were successfully scraped.[/]")

    console.print("\n[bold cyan]=== Thank you for using Learn4Free! ===[/]", justify="center")

if __name__ == "__main__":
    main()
