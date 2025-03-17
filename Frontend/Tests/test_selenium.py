# frontend/tests/test_selenium.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest

# Fixture to initialize and close the browser
@pytest.fixture(scope="module")
def browser():
    # Initialize the browser (e.g., Chrome)
    driver = webdriver.Firefox()  # Or specify the path to the driver: webdriver.Chrome('/path/to/chromedriver')
    yield driver
    # Close the browser after the tests
    driver.quit()

# Test: Add a task and verify it is displayed
def test_add_task(browser):
    # Open the Task Tracker App
    browser.get("http://127.0.0.1:5500/index.html")
    
    # Debugging: Print page source or take a screenshot
    print(browser.page_source)
    browser.save_screenshot("before_interaction.png")
    
    # Wait for the form elements to be present
    topic_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "topic"))
    )
    title_input = browser.find_element(By.ID, "title")
    description_input = browser.find_element(By.ID, "description")
    time_start_input = browser.find_element(By.ID, "time-start")
    time_end_input = browser.find_element(By.ID, "time-end")
    dependencies_input = browser.find_element(By.ID, "dependencies")
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    # Fill out the form
    topic_input.send_keys("Test Topic")
    title_input.send_keys("Test Task")
    description_input.send_keys("Test Description")
    time_start_input.send_keys("2023-10-01T09:00")
    time_end_input.send_keys("2023-10-01T12:00")
    dependencies_input.send_keys("1")
    
    # Submit the form
    submit_button.click()
    
    # Wait for the task to appear in the list
    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.ID, "task-list"), "Test Topic: Test Task")
    )
    
    # Verify the task is displayed
    task_list = browser.find_element(By.ID, "task-list")
    assert "Test Topic: Test Task" in task_list.text



# Test: Delete a task and verify it is removed
def test_delete_task(browser):
    # Open the Task Tracker App
    browser.get("http://127.0.0.1:5500/frontend/index.html")  # Update the URL if needed

    # Add a task first (you can reuse the code from test_add_task)
    browser.find_element(By.CSS_SELECTOR, "topic").send_keys("Test Topic")
    browser.find_element(By.ID, "title").send_keys("Test Task")
    browser.find_element(By.ID, "description").send_keys("Test Description")
    browser.find_element(By.ID, "time-start").send_keys("2023-10-01T09:00")
    browser.find_element(By.ID, "time-end").send_keys("2023-10-01T12:00")
    browser.find_element(By.ID, "dependencies").send_keys("")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

    # Delete the task
    delete_button = browser.find_element(By.CSS_SELECTOR, "#task-list li button")
    delete_button.click()

    # Wait for the task to be deleted
    time.sleep(2)

    # Verify the task is no longer in the list
    task_list = browser.find_element(By.ID, "task-list")
    assert "Test Topic: Test Task" not in task_list.text