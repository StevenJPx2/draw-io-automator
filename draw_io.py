import os
import re
from argparse import ArgumentParser

import selenium
from selenium import webdriver

CURRENT_PATH = os.getcwd()
WAIT_TIME = 5

def create_parser():
    parser = ArgumentParser()
    
    parser.add_argument('filepath', help="Create drawio file in given filepath", nargs="?", default=r"Untitled\ Diagram.drawio")
    parser.add_argument('-v', '--verbose', help="Verbose mode", action="store_true")

    return parser

def draw_io_file(file_path, v):
    driver = webdriver.Firefox()
    driver.get('https://draw.io/')
    driver.implicitly_wait(WAIT_TIME)
    if v: print("Page is assumed to be fully loaded.")
    try:
        driver.find_element_by_link_text('Device').click()
        if v: print("Selected 'Device' as storage option.")
    except selenium.common.exceptions.NoSuchElementException as e:
        if v: print(e)
    if not re.match(r'.*\.drawio', file_path): file_path += ".drawio"
    driver.find_element_by_xpath('//button[@class="geBigButton"][1]').click()
    if v: print("'Create New Diagram' button selected.")
    driver.find_element_by_xpath('//input[@value="Untitled Diagram.drawio"]').send_keys(file_path)
    if v: print("Changed name of diagram.")
    driver.find_element_by_xpath('//button[@class="geBtn gePrimaryBtn"][text()="Create"]').click()
    if v: print("Created drawio file successfully.")
    
def main():
    parser = create_parser()
    args = parser.parse_args()
    
    file_path = args.filepath
    
    split_file_path = os.path.split(file_path)
    
    try:
        os.chdir(split_file_path[0])     
    except FileNotFoundError:
        os.chdir(CURRENT_PATH)
    
    draw_io_file(split_file_path[1].replace(r'\ ', ' '), args.verbose)
    
    
if __name__ == "__main__":
    main()
