import requests # For making HTTP requests to fetch page content
import pyperclip # For copying text to the clipboard
import re # For regular expression matching
import sys 

# Note: You may need to install the following libraries if you haven't already:
# pip install requests pyperclip

def main_loop():
    """
    Runs a continuous loop to prompt the user for JUPAS codes, 
    fetches the page title, and copies the title to the clipboard.
    """
    # Mapping the first digit of the program code to the university slug
    university_map = {
        '4': 'cuhk',    # Chinese University of Hong Kong
        '5': 'hkust',   # Hong Kong University of Science and Technology
        '6': 'hku',     # The University of Hong Kong
        '1': 'cityuhk', # City University of Hong Kong
        '3': 'polyu'    # The Hong Kong Polytechnic University
    }
    
    print("JUPAS Title Fetcher is running.")
    print("Enter 'quit' or 'exit' to stop the program.\n")

    while True:
        # Get input from the user
        s = input("Enter a 4-digit JUPAS program number: ").strip().lower()

        # Check for exit command
        if s in ('quit', 'exit'):
            print("\nExiting JUPAS Title Fetcher. Goodbye!")
            break

        # Input validation
        if not s.isdigit() or len(s) != 4:
            print(f"\n[ERROR] Input must be exactly a 4-digit number. You entered: '{s}'")
            print("-" * 20)
            continue # Go back to the start of the loop

        first_digit = s[0]

        if first_digit not in university_map:
            print(f"\n[ERROR] The first digit '{first_digit}' does not correspond to a mapped university code (1, 3, 4, 5, 6).")
            print("-" * 20)
            continue # Go back to the start of the loop

        # 1. Determine the university part
        school_slug = university_map[first_digit]

        # 2. Determine the code part
        program_code = f"JS{s}"

        # 3. Construct the final URL
        url = f"https://www.jupas.edu.hk/en/programme/{school_slug}/{program_code}/"

        print("\n--- Processing ---")
        print(f"Code: {s} | University: {school_slug.upper()}")
        print(f"URL: {url}")
        
        # 4. Fetch the webpage content
        try:
            print("Fetching webpage content...")
            # Use a short timeout to prevent hanging indefinitely
            response = requests.get(url, timeout=10)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            html_content = response.text

        except requests.exceptions.HTTPError as err:
            print(f"\n[FETCH ERROR] Failed to fetch the URL due to HTTP error: {err}")
            print("-" * 20)
            continue
        except requests.exceptions.ConnectionError:
            print("\n[FETCH ERROR] Could not connect to the JUPAS website. Check your internet connection.")
            print("-" * 20)
            continue
        except requests.exceptions.Timeout:
            print("\n[FETCH ERROR] Request timed out while connecting to the JUPAS website.")
            print("-" * 20)
            continue
        except Exception as e:
            print(f"\n[UNEXPECTED ERROR] An unexpected error occurred during fetching: {e}")
            print("-" * 20)
            continue

        # 5. Extract the <title> content using a regular expression
        # This regex captures content between <title> and </title> tags
        title_match = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)

        if title_match:
            # Extract the captured group (the content inside the tags)
            page_title = title_match.group(1).strip()
            
            # 6. Copy the title to the clipboard
            try:
                pyperclip.copy(page_title)
                
                print(f"\n[SUCCESS] Title copied to clipboard:")
                print(f"Title: \"{page_title}\"")
                print("-" * 20)
            
            except pyperclip.PyperclipException:
                print(f"\n[CLIPBOARD ERROR] Could not access the system clipboard.")
                print(f"The title is: \"{page_title}\"")
                print("-" * 20)

        else:
            print("\n[PARSE ERROR] Could not find the <title> tag in the webpage content.")
            print("This usually means the program code is invalid or the page doesn't exist.")
            print("-" * 20)

if __name__ == "__main__":
    main_loop()
