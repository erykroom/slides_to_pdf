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
```

## Script Details

The script performs the following tasks:

1. **Setup WebDriver:** Configures and launches a headless Firefox browser.
2. **Capture Slides:** Navigates through the slides and captures screenshots.
3. **Generate PDF:** Compiles the screenshots into a single PDF file.
4. **Cleanup:** Removes temporary screenshot files.

### Functions

- **`setup_driver(url):`** Configures the Firefox WebDriver.
- **`take_screenshot(driver, page, save_path):`** Captures a screenshot of the current slide.
- **`capture_presentation(url, save_path):`** Orchestrates the process of capturing all slides.
- **`create_pdf(save_path, filename="myslides"):`** Creates a PDF from the captured screenshots.
- **`remove_temp_files(save_path):`** Removes temporary screenshot files.
- **`main(slides_url, save_path):`** Main function to run the script.
