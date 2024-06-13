# slides_to_pdf

This script captures slides from a given Slides.com presentation URL and converts them into a PDF file. The script uses Selenium for web automation, PIL for image processing, and FPDF for PDF generation.

## Requirements

- Python 3.6+
- Firefox Browser
- Geckodriver (for Firefox WebDriver)
- Required Python packages (can be installed via `requirements.txt`)

## Installation

1. **Clone the repository:**

    ```sh
    git clone ...
    cd slides_to_pdf
    ```

2. **Set up a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install the required Python packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Ensure Firefox and Geckodriver are installed:**

    - **For Firefox:**
      - Download and install from [Mozilla's website](https://www.mozilla.org/en-US/firefox/new/).
    
    - **For Geckodriver:**
      - Download from [Geckodriver releases](https://github.com/mozilla/geckodriver/releases).
      - Make sure the geckodriver executable is in your system's PATH.

## Usage

Run the script with the following command:

```sh
python src/slides_refactor.py <slides_url> --save-path <save_path>
