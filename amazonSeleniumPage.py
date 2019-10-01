'''Python program to add amazon bestseller headphones to cart
'''
import time
from selenium import webdriver

def main():
    '''main program to add amazon bestsellers headphones to cart
    input: None:
    output: Bestseller Headphones added to cart
    '''
    baseurl = "https://www.amazon.com"

    # declare and initialize driver variable
    driver = webdriver.Chrome(executable_path='//usr//local//bin//chromedriver')
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get(baseurl)

    # test whether correct URL/ Web Site has been loaded or not
    assert "Amazon" in driver.title

    # declare variable to store search term
    search = "Headphones"
    driver.find_element_by_id("twotabsearchtextbox").send_keys(search)

    # search button xpath
    searchbutton = "//div[@class='nav-search-submit nav-sprite']//input[@class='nav-input']"
    driver.find_element_by_xpath(searchbutton).click()

    # test if the search results page loaded
    assert f"Amazon.com: {search}" in driver.title

    # test if the search results page contains any results or no results were found.
    assert "No results found." not in driver.page_source

    # find all bestseller items
    bestsellers = driver.find_elements_by_xpath(("//span[text()='Best Seller']" +
     		                           "/ancestor::div[@data-asin and not(.//span[.='Sponsored'])][1]" +
     		                           "//span[@data-component-type='s-product-image']//a"))
    

    # get href for all bestseller items
    new_links = []
    for item in bestsellers:
        new_links.append(item.get_attribute('href'))

    print("No of bestseller on page:", len(new_links))

    # iterate through all bestseller items and put it in the cart
    for link in new_links:
        print("Adding this item to the cart:", link)
        driver.get(link)
        driver.find_element_by_id("add-to-cart-button").click()

        # add 3 year protection pop up handline: model dialog or warranty pane.
        if driver.find_elements_by_xpath("//div[@class='a-popover-wrapper']"):
            driver.find_element_by_id("siNoCoverage-announce").click()
        elif driver.find_elements_by_xpath("//div[@id='attach-warranty-pane']"):
            driver.find_element_by_id("attachSiNoCoverage-announce").click()
        else:
            pass

        # to handle Added to cart visibility
        time.sleep(2)
        assert "Added to Cart" in driver.page_source

    time.sleep(1)
    driver.close()

if __name__ == "__main__":
	main()
