import webbrowser
import sys

def open_jupas_link():
    """
    Prompts the user for a 4-digit JUPAS code, constructs the corresponding 
    university program link, and opens it in the default web browser.
    """
    # Mapping the first digit of the program code to the university slug
    university_map = {
        '4': 'cuhk',    # Chinese University of Hong Kong
        '5': 'hkust',   # Hong Kong University of Science and Technology
        '6': 'hku',     # The University of Hong Kong
        '1': 'cityuhk', # City University of Hong Kong
        '3': 'polyu'    # The Hong Kong Polytechnic University
    }

    # Get input from the user
    s = input("Enter a 4-digit JUPAS program number (e.g., 6303 or 5240): ").strip()

    # Input validation
    if not s.isdigit() or len(s) != 4:
        print(f"\nError: Input must be exactly a 4-digit number. You entered: '{s}'")
        # Exit the function if validation fails
        return

    first_digit = s[0]

    if first_digit not in university_map:
        print(f"\nError: The first digit '{first_digit}' does not correspond to a mapped university code (1, 3, 4, 5, 6).")
        return

    # 1. Determine the university part
    school_slug = university_map[first_digit]

    # 2. Determine the code part
    program_code = f"JS{s}"

    # 3. Construct the final URL
    url = f"https://www.jupas.edu.hk/en/programme/{school_slug}/{program_code}/"

    print("\n---")
    print(f"Input program code: {s}")
    print(f"Detected University: {school_slug.upper()}")
    print(f"Generated URL: {url}")
    print("---")
    
    # 4. Open the link in the default browser
    try:
        webbrowser.open_new_tab(url)
        print("\nOpening link in your default web browser...")
    except Exception as e:
        print(f"\nFailed to open web browser. Please open the URL manually.")
        print(f"Details: {e}")

if __name__ == "__main__":
    open_jupas_link()
