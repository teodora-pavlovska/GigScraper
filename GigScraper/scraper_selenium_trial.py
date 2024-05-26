from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from fpdf import FPDF

NEARBY_AND_CHEAP = [
    "Athens", "Thessaloniki", "Greece",
    "Belgrade", "Serbia",
    "Sofia", "Bulgaria",
    "Bucharest", "Romania",
    "Budapest", "Hungary",
    "Vienna", "Austria",
    "Zagreb", "Croatia",
    "Sarajevo", "Bosnia and Herzegovina",
    "Podgorica", "Montenegro",
    "Pristina", "Kosovo",
    "Tirana", "Albania",
    "Istanbul", "Turkey",
    "Skopje", "North Macedonia",
    "Ljubljana", "Slovenia",
    "Rome", "Italy",
    "Milan", "Italy",
    "Lisbon", "Portugal",
    "Amsterdam", "Netherlands",
    "Barcelona", "Berlin", "Frankfurt"
]

LAUV_INFO = ('Lauv', 'https://www.lauvsongs.com/#tour')
MITSKI_INFO = ('Mitski', 'https://mitski.com/')
SWIFT_INFO = ('Taylor Swift', 'https://www.taylorswift.com/tour/')

def fetch_seated_events(artist_name, gigs_info):
    driver_path = 'C:\\Users\\astra\\Desktop\\WbDriver\\msedgedriver.exe'
    service = Service(driver_path)

    driver = webdriver.Edge(service=service)
    driver.get(gigs_info)

    tour_dates_list = []
    try:
        wait = WebDriverWait(driver, 10)
        tour_dates_section = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".seated-events-table"))
        )

        tour_dates = tour_dates_section.find_elements(By.CSS_SELECTOR, ".seated-event-row")

        for event in tour_dates:
            date = event.find_element(By.CSS_SELECTOR, ".seated-event-date-cell").text.strip()
            venue = event.find_element(By.CSS_SELECTOR, ".seated-event-venue-name").text.strip()
            location = event.find_element(By.CSS_SELECTOR, ".seated-event-venue-location").text.strip()
            details = event.find_element(By.CSS_SELECTOR, ".seated-event-details-cell").text.strip()
            tour_dates_list.append({'artist': artist_name, 'date': date, 'venue': venue, 'location': location, 'details': details})
    except NoSuchElementException:
        print(f"Some elements were not found in {gigs_info}")
    finally:
        driver.quit()

    return tour_dates_list

def fetch_tour_dates_Taylors_Version():
    # Path to your Edge WebDriver
    driver_path = 'C:\\Users\\astra\\Desktop\\WbDriver\\msedgedriver.exe'
    service = Service(driver_path)

    driver = webdriver.Edge(service=service)
    driver.get('https://www.taylorswift.com/tour/')

    try:

        wait = WebDriverWait(driver, 20)  # Increased wait time to 20 seconds
        try:
            tour_grid_container = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".tour-grid--container"))
            )
        except TimeoutException:
            print("tour-grid--container not found.")
            print(driver.page_source)
            driver.quit()
            return []

        tour_dates = tour_grid_container.find_elements(By.CSS_SELECTOR, ".tour-grid--item.international")

        tour_dates_list = []
        for event in tour_dates:
            try:
                date = event.find_element(By.CSS_SELECTOR, ".tour-date.tour-international-table-row-date").text.strip()
                venue = event.find_element(By.CSS_SELECTOR, ".tour-venue.tour-international-table-row-venue.venue-lineup").text.strip()
                city = event.find_element(By.CSS_SELECTOR, ".tour-city.tour-international-table-row-city").text.strip()
                tour_dates_list.append({'artist': "Taylor Swift", 'date': date, 'venue': venue, 'location': city, 'details': "no info"})
            except NoSuchElementException as e:
                print(f"Error extracting data for an event: {e}")

    finally:
        driver.quit()

    return tour_dates_list

def fetch_tour_dates_RHCP_edition():

    driver_path = 'C:\\Users\\astra\\Desktop\\WbDriver\\msedgedriver.exe'  # Ensure this path is correct
    service = Service(driver_path)

    driver = webdriver.Edge(service=service)
    driver.get('https://redhotchilipeppers.com/tour/')

    try:
        wait = WebDriverWait(driver, 10)
        tour_dates_section = wait.until(
            EC.presence_of_element_located((By.ID, "tours-list"))
        )

        rows = tour_dates_section.find_elements(By.CSS_SELECTOR, ".row.pb-5")

        tour_dates_list = []
        for row in rows:
            date = row.find_elements(By.CSS_SELECTOR, ".col-md-4.text-center")[0].text.strip()
            venue = row.find_elements(By.CSS_SELECTOR, ".col-md-4.text-center")[1].text.strip()
            tour_dates_list.append(
                {'artist': "Red Hot Chilli Peppers", 'date': date.upper(), 'venue': venue, 'location': '', 'details': "no info"})

    finally:
        driver.quit()

    return tour_dates_list
def save_tour_dates_to_pdf(tours, filename='tour_dates.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Tour Dates", ln=True, align='C')

    current_artist = None
    for event in tours:
        if event['artist'] != current_artist:
            current_artist = event['artist']
            pdf.set_font("Arial", size=14, style='B')
            pdf.cell(200, 10, txt=current_artist, ln=True, align='L')
            pdf.set_font("Arial", size=12)

        event_text = f"{event['date']} - {event['venue']}, {event['location']}"
        is_close = any(
            city_country.lower() in event['location'].lower() or city_country.lower() in event['venue'].lower() for city_country in NEARBY_AND_CHEAP
        )

        if is_close:
            pdf.set_text_color(255, 0, 0)
            pdf.set_font("Arial", size=12, style='B')
        else:
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=event_text, ln=True, align='L')

    pdf.output(filename)



if __name__ == '__main__':
    tours = []
    tour_dates_mitski = fetch_seated_events(*MITSKI_INFO)
    tours.extend(tour_dates_mitski)
    tour_dates_lauv = fetch_seated_events(*LAUV_INFO)
    tours.extend(tour_dates_lauv)
    tour_dates_taylors_version = fetch_tour_dates_Taylors_Version()
    tours.extend(tour_dates_taylors_version)
    tds_rhcp= fetch_tour_dates_RHCP_edition()
    tours.extend(tds_rhcp)

    if tours:
        save_tour_dates_to_pdf(tours)
        print("Tour dates have been saved to 'tour_dates.pdf'")
    else:
        print("No tour dates found.")
