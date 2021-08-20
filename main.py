# Technical Assessment- Vikramjeet
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AssessmentTestCase(unittest.TestCase):

    def setUp(self):
        """Chrome browser instance."""
        self.browser = webdriver.Chrome('/usr/bin/chromedriver')
        self.browser.implicitly_wait(10)
        self.browser.set_window_size(1920, 1080)
        self.addCleanup(self.browser.quit)

    def test_case_1(self):
        """
        1. From the home page go to contact page
        2. Click submit button
        3. Validate errors
        4. Populate mandatory fields
        5. Validate errors are gone
        """
        self.browser.get('https://jupiter.cloud.planittesting.com')
        self.browser.find_element_by_link_text('Contact').click()   # Go To Contact page
        self.browser.find_element_by_link_text('Submit').click()      # click submit button

        error_dict = {'forename-err': 'Forename is required', 'email-err': 'Email is required', 'message-err': 'Message is required'}
        for err in error_dict:
            element = self.browser.find_element_by_id(err)
            self.assertEqual(error_dict[err], element.text, msg='Error String mismatch')
        fields_dict = {'forename': 'John', 'email': 'john@gmail.com', 'message': 'message from John'}
        for field in fields_dict:
            element = self.browser.find_element_by_id(field)
            element.send_keys(fields_dict[field])
            element = self.browser.find_element_by_id(field)
            element.click()
            assert element is not None
            self.assertEqual(fields_dict[field], element.get_attribute('value'))
        for err in error_dict:
            try:
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, err)))
                not_found = False
            except:
                not_found = True
            assert not_found

    def test_case_2(self):
        """
        1. From the home page go to contact page
        2. Populate mandatory fields
        3. Click submit button
        4. Validate successful submission message
        """
        self.browser.get('https://jupiter.cloud.planittesting.com')
        self.browser.find_element_by_link_text('Contact').click()   # Go To Contact page

        fields_dict = {'forename': 'John', 'email': 'john@gmail.com', 'message': 'message from John'}
        for field in fields_dict:
            element = self.browser.find_element_by_id(field)
            element.send_keys(fields_dict[field])
            element = self.browser.find_element_by_id(field)
            element.click()
        self.browser.find_element_by_link_text('Submit').click()
        WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert > .ng-binding")))
        text_forename = self.browser.find_element_by_xpath("//strong").text
        self.assertEqual('Thanks '+fields_dict['forename'], text_forename)

    def test_case_3(self):
        """
        1. From the home page go to shop page
        2. Click buy button 2 times on “Funny Cow”
        3. Click buy button 1 time on “Fluffy Bunny”
        4. Click the cart menu
        5. Verify the items are in the cart
        """
        self.browser.get('https://jupiter.cloud.planittesting.com')
        self.browser.find_element_by_link_text('Shop').click()  # Go To Contact page

        product_elems = self.browser.find_elements_by_xpath("//*[@ng-repeat='item in catalog']")
        product_dict = {}
        for element in product_elems:
            p_id = element.get_attribute('id')
            p_title = self.browser.find_element_by_xpath('//*[@id=\"' + p_id + '\"]/div/h4').text
            p_cost = self.browser.find_element_by_xpath('//*[@id=\"' + p_id + '\"]/div/p/span').text
            product_dict[p_title] = [p_id, p_cost]

        self.browser.find_element_by_xpath('//*[@id=\"' + product_dict['Funny Cow'][0] + '\"]/div/p/a').click()
        self.browser.find_element_by_xpath('//*[@id=\"' + product_dict['Funny Cow'][0] + '\"]/div/p/a').click()
        self.browser.find_element_by_xpath('//*[@id=\"' + product_dict['Fluffy Bunny'][0] + '\"]/div/p/a').click()

        num_of_items = self.browser.find_element_by_xpath('//li[@id="nav-cart"]/a').text
        self.assertEqual(num_of_items, 'Cart (3)')
        self.browser.find_element_by_xpath('//li[@id="nav-cart"]/a').click()

        items_in_cart = self.browser.find_elements_by_xpath("//*[@ng-repeat='item in cart.items()']")
        cart_item_names = []
        for item_row in items_in_cart:
            cart_item_names.append(item_row.text.rsplit(' ', 2)[0])
        self.assertIn('Funny Cow', cart_item_names)
        self.assertIn('Fluffy Bunny', cart_item_names)

    def test_case_4(self):
        """
        1. Buy 2 Stuffed Frog, 5 Fluffy Bunny, 3 Valentine Bear
        2. Go to the cart page
        3. Verify the price for each product
        4. Verify that each product’s sub total = product price * quantity
        5. Verify that total = sum(sub totals)
        """
        self.browser.get('https://jupiter.cloud.planittesting.com')
        self.browser.find_element_by_link_text('Shop').click()  # Go To Contact page

        product_elems = self.browser.find_elements_by_xpath("//*[@ng-repeat='item in catalog']")
        product_dict = {}
        for element in product_elems:
            p_id = element.get_attribute('id')
            p_title = self.browser.find_element_by_xpath('//*[@id=\"' + p_id + '\"]/div/h4').text
            p_cost = self.browser.find_element_by_xpath('//*[@id=\"' + p_id + '\"]/div/p/span').text
            product_dict[p_title] = [p_id, p_cost]
        names_count = {'Stuffed Frog': 2, 'Fluffy Bunny': 5, 'Valentine Bear': 3}
        for name in names_count:
            count = names_count[name]
            for c in range(count):
                self.browser.find_element_by_xpath('//*[@id=\"' + product_dict[name][0] + '\"]/div/p/a').click()
        self.browser.find_element_by_xpath('//li[@id="nav-cart"]/a').click()
        items_in_cart = self.browser.find_elements_by_xpath("//*[@ng-repeat='item in cart.items()']")

        total_list = []
        for item_row in items_in_cart:
            name = item_row.text.rsplit(' ', 2)[0]
            price = item_row.text.rsplit(' ', 2)[1]
            subtotal = item_row.text.rsplit(' ', 2)[2]
            # Verify Price for each product
            self.assertEqual(price, product_dict[name][1])
            # Verify Subtotal
            calculated_subtotal = '$'+str(float(price.strip('$')) * float(names_count[name]))
            self.assertEqual(calculated_subtotal, subtotal)
            total_list.append(float(subtotal.strip('$')))
        # Verify Total
        calculated_total = sum(total_list)
        total_from_items_page = self.browser.find_element_by_css_selector(".total").text
        self.assertEqual('Total: ' + str(calculated_total), total_from_items_page)



if __name__ == '__main__':
    unittest.main(verbosity=2)
