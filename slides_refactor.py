import argparse
import os
import time
import datetime
import logging
from fpdf import FPDF
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def setup_driver(url):
    """Setup the Firefox WebDriver."""
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    wd = webdriver.Firefox(options=opts)
    time.sleep(2)

    try:
        wd.get(url)
    except WebDriverException as e:
        wd.quit()
        logging.error(f"Failed to load URL: {e}")
        raise
    scripts = [
        "var el = document.getElementsByClassName('pill'); el[0].remove(); el[0].remove();",
        "var el = document.getElementsByClassName('kudos-button'); el[0].remove();",
        "var el = document.getElementsByClassName('progress'); el[0].remove();",
        "var el = document.getElementsByClassName('fullscreen-button'); el[0].removeAttribute('data-tooltip');",
    ]
    for script in scripts:
        wd.execute_script(script)
    return wd


def take_screenshot(driver, page, save_path):
    """Take a screenshot of the current view."""
    try:
        element = driver.find_element(By.CLASS_NAME, "backgrounds")
        location = element.location
        size = element.size
        png = driver.get_screenshot_as_png()

        im = Image.open(BytesIO(png))

        left = location["x"]
        top = location["y"]
        right = location["x"] + size["width"]
        bottom = location["y"] + size["height"]

        im = im.crop((left, top, right, bottom))
        screenshot_path = os.path.join(save_path, f"screenshot_{page}.png")
        im.save(screenshot_path)
        logging.info(f"Screenshot saved as {screenshot_path}")
    except Exception as e:
        logging.error(f"An error occurred while taking screenshot: {e}")
        raise


def capture_presentation(url, save_path):
    """Capture all slides from the presentation."""
    driver = setup_driver(url)
    presentation = True
    page = 1

    driver.find_element(By.CLASS_NAME, "fullscreen-button").click()
    while presentation:
        down = driver.find_element(By.CLASS_NAME, "navigate-down")
        right = driver.find_element(By.CLASS_NAME, "navigate-right")

        if down.is_enabled():
            take_screenshot(driver, str(page).zfill(2), save_path)
            down.click()
            time.sleep(2)
            page += 1
        elif right.is_enabled():
            take_screenshot(driver, str(page).zfill(2), save_path)
            right.click()
            time.sleep(2)
            page += 1
        else:
            take_screenshot(driver, str(page).zfill(2), save_path)
            presentation = False

    driver.quit()


def create_pdf(save_path, filename="myslides"):
    """Create a PDF from the captured slides."""
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_dir = os.path.join(save_path, "result")
    os.makedirs(output_dir, exist_ok=True)
    pdf_filename = os.path.join(output_dir, f"{now}_{filename}.pdf")
    images = sorted(
        [
            f
            for f in os.listdir(save_path)
            if f.startswith("screenshot") and f.endswith(".png")
        ]
    )

    if not images:
        logging.error("No screenshots found to create PDF.")
        return

    first_image = Image.open(os.path.join(save_path, images[0]))
    width, height = first_image.size

    pdf = FPDF("L", "mm", (height, width))
    pdf.set_margins(0, 0, 0)
    for image in images:
        pdf.add_page()
        pdf.image(os.path.join(save_path, image), y=0, w=width)
    pdf.output(pdf_filename, "F")
    logging.info(f"PDF saved as {pdf_filename}")


def remove_temp_files(save_path):
    """Remove temporary files."""
    for filename in os.listdir(save_path):
        if filename.startswith("screenshot") and filename.endswith(".png"):
            os.remove(os.path.join(save_path, filename))
    logging.info("Temporary files removed")


def main(slides_url, save_path):
    """Main function to orchestrate the capture, PDF creation, and cleanup."""
    os.makedirs(save_path, exist_ok=True)
    logging.info("Starting presentation capture")
    capture_presentation(slides_url, save_path)
    logging.info("Creating PDF")
    create_pdf(save_path)
    logging.info("Removing intermediate files")
    remove_temp_files(save_path)
    logging.info("Process completed")


if __name__ == "__main__":
    description = "Create PDF files from slides.com presentation"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("slidesurl", metavar="s", type=str, help="URL for the slides")
    parser.add_argument(
        "--save-path",
        metavar="p",
        type=str,
        help="Path to save the slides",
        default="./slides",
    )
    args = parser.parse_args()

    main(args.slidesurl, args.save_path)
