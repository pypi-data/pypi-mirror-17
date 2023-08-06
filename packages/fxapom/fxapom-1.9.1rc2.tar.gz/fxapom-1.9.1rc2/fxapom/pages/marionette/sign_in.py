# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import expected, Wait, By

from fxapom.fxapom import TIMEOUT
from fxapom.pages.marionette.base import Base


class MarionetteSignIn(Base):

    _fox_logo_locator = (By.ID, 'fox-logo')
    _email_input_locator = (By.CSS_SELECTOR, '.input-row .email')
    _next_button_locator = (By.ID, 'email-button')
    _password_input_locator = (By.ID, 'password')
    _sign_in_locator = (By.ID, 'submit-btn')

    def __init__(self, driver, timeout=TIMEOUT):
        super(Base, self).__init__(driver, timeout)
        self._sign_in_window_handle = None
        self.popup = False
        self.check_for_popup(self.driver.window_handles)

    @property
    def email(self):
        """Get the value of the email field."""
        return self.driver.find_element(*self._email_input_locator).get_attribute('value')

    @email.setter
    def email(self, value):
        """Set the value of the email field."""
        email = Wait(self.driver, self.timeout).until(
            expected.element_present(*self._email_input_locator))
        Wait(self.driver, self.timeout).until(
            expected.element_displayed(email))
        email.clear()
        email.send_keys(value)

    @property
    def login_password(self):
        """Get the value of the login password field."""
        return self.driver.find_element(*self._password_input_locator).get_attribute('value')

    @login_password.setter
    def login_password(self, value):
        """Set the value of the login password field."""
        password = self.driver.find_element(*self._password_input_locator)
        password.clear()
        password.send_keys(value)

    def click_next(self):
        self.driver.find_element(*self._next_button_locator).click()

    def check_for_popup(self, handles):
        if len(self.driver.window_handles) > 1:
            self.popup = True
            for handle in handles:
                self.driver.switch_to.window(handle)
                if self.is_element_visible(*self._fox_logo_locator):
                    Wait(self.driver, self.timeout).until(
                        expected.element_displayed(*self._email_input_locator))
                    self._sign_in_window_handle = handle
                    break
            else:
                raise Exception('Popup has not loaded')

    def click_sign_in(self):
            self.driver.find_element(*self._sign_in_locator).click()
            if self.popup:
                Wait(self.driver, self.timeout).until(
                    lambda s: self._sign_in_window_handle not in self.driver.window_handles)
                self.switch_to_main_window()

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        self.email = email
        self.login_password = password
        if self.is_element_visible(*self._next_button_locator):
            self.click_next()
        self.click_sign_in()
