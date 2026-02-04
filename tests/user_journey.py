from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        

        page.goto("http://localhost:5000/api/users")
        print("Page Title:", page.title())
        
        content = page.content()
        if "python_tester" in content:
            print("E2E Test Passed: Initial data found.")
        else:
            print("E2E Test Failed: Data not found.")
            
        browser.close()

if __name__ == "__main__":
    run_test()