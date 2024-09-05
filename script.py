from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd


@dataclass
class Business:
    name: str = None
    address: str = None
    phone: str = None
    web: str = None
    ratings: str = None

@dataclass
class BusinessList:
    business_list: list[Business] = field(default_factory=list)

    def data_frame(self):
        return pd.json_normalize((asdict(business) for business in self.business_list), sep="|")
    
    def save_to_excel(self, filename):
        self.data_frame().to_excel(f'{filename}.xlsx', index=False)

def get_text_content(page, xpath, use_aria_label=True):
    try:
        if not use_aria_label:
            page.wait_for_selector(xpath, timeout=3500)
            return page.locator(xpath).text_content()

        else:
            page.wait_for_selector(xpath, timeout=3500)
            return page.locator(xpath).get_attribute('aria-label')

    except Exception as e:
        print(e)
        return None

def main(output_file, num_of_listing):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto('https://www.google.com/maps', timeout=60000)
        page.wait_for_timeout(5000)
        print("loading th page........")

        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.wait_for_timeout(3000)

        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)

        # page.hover("(//div[@class='Nv2PK THOPZb CpccDe '])[1]")
        page.hover("(//div[contains(@class, 'THOPZb ')])[1]")
        
        while True:
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(3000)
            try:
                page.wait_for_selector("//span[contains(text(), \"You've reached the end of the list.\")]", timeout=2500)
                print("Reached the end of the list. Exiting the loop.")
                break
            except Exception as e:
                print(e) 
                pass
            
            listings = page.locator("//div[contains(@class, 'THOPZb ')]").all()
            print(len(listings), "Total LISTINGS!!!!-----------")
            if num_of_listing:
                if len(listings) >= num_of_listing:
                    listings = listings[:num_of_listing]
                    print(f"Scraping ONLY {num_of_listing} LISTINGS---------")
                    break

        business_list = BusinessList()
        i ,j= 0, len(listings)

        for listing in listings:
            i += 1
            j -= 1
            print()
            print('extracting data from listing...')
            print()
            listing.click()
            page.wait_for_timeout(5000)
            
            name = get_text_content(page, '//h1[@class="DUwDvf lfPIob"]', use_aria_label=False)
            address = get_text_content(page, '//button[@data-item-id="address"]')
            web = get_text_content(page, '//a[@data-item-id="authority"]')  
            phone = get_text_content(page, '(//button[@data-tooltip="Copy phone number"])[1]')
            ratings = get_text_content(page, '//div[@class="F7nice "]//span[@aria-hidden="true"]', use_aria_label=False)

            print(f"Name: {name}")
            print(address)
            print(web)
            print(phone)
            print(f"Ratings: {ratings}/5")
            print()
            print(f'{i}/{len(listings)} 🛠️ scraped,  {j} remaining.....')

            business = Business()
            
            business.name = name
            
            business.address = address[9:] if address else None
            business.web = web[9:] if web else None
            business.phone = phone[7:] if phone else None
            business.ratings = ratings if ratings else None

            business_list.business_list.append(business)

        business_list.save_to_excel(output_file)
            
        browser.close()

if __name__ == "__main__":
    search_for = "Architects in paschim vihar"

    slug = search_for.replace(" ", "_").lower()
    output_file = f'DEL_LJPT/{slug}.txt'

    main(output_file=output_file, num_of_listing=None)  
    # put num_of_listing = None if you want all the listings, otherwise put your desired number