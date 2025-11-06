from playwright.sync_api import Page, expect
import os
import re

def test_email_validation(page: Page):
    """
    This test verifies that the email validation for the admin email settings works correctly.
    """
    # 1. Arrange: Go to the index.html page.
    file_path = "file://" + os.path.abspath("index.html")
    page.goto(file_path)

    # 2. Act & Assert (Invalid Email):
    email_input = page.locator("#admin-email-input")
    save_button = page.get_by_role("button", name="Save Email")
    message_box = page.locator("#message-box")

    # Test with an invalid email
    email_input.fill("invalid-email")
    save_button.click()
    expect(message_box).to_have_text("Please enter a valid email address.")
    expect(message_box).to_have_class(re.compile(r"bg-red-600"))

    # 3. Act & Assert (Valid Email):
    # Test with a valid email
    # A different valid email to avoid the "already saved" message
    email_input.fill("another.valid.email@example.com")
    save_button.click()

    # The original function fails in a file:// context because Firebase isn't initialized.
    # So we check for either the success message or the firebase error.
    # This still validates the initial regex check passed.
    try:
        expect(message_box).to_have_text("Notification email set to: another.valid.email@example.com")
        expect(message_box).to_have_class(re.compile(r"bg-green-600"))
    except AssertionError:
        expect(message_box).to_have_text("Error saving notification email.")
        expect(message_box).to_have_class(re.compile(r"bg-red-600"))
