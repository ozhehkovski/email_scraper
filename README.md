# Website Contact Information Scraper

**Description:**
The Website Contact Information Scraper is a Python tool developed using Scrapy, designed to search for contact email addresses, determine Content Management Systems (CMS), and collect links to social media profiles on specified websites. This versatile web scraping tool automates the process of extracting valuable contact information and CMS details, enabling users to streamline their outreach efforts, gather insights into website technologies, and enhance their social media presence.

**Features:**
1. **Email Extraction:** Automatically search web pages for contact email addresses, helping users quickly locate primary points of contact for businesses or individuals.
2. **CMS Detection:** Identify the Content Management System (CMS) used to build the website, providing insights into the underlying technologies and facilitating compatibility assessment for integration or development purposes.
3. **Social Media Link Collection:** Gather links to social media profiles associated with the website, allowing users to easily connect with the website owners or administrators on various social platforms.
4. **Customizable Website List:** Specify the websites to be scanned for contact information, allowing users to target specific domains or URLs of interest.
5. **Scalability:** The scraper is capable of handling multiple websites and large volumes of data, making it suitable for both small-scale and enterprise-level projects.
6. **Proxy Support:** Configure proxies to bypass rate limiting and ensure uninterrupted scraping sessions, enhancing the tool's reliability and performance.
7. **Robust Error Handling:** Built-in error handling mechanisms to manage unexpected scenarios and ensure smooth operation, minimizing disruptions during the scraping process.

**Requirements:**
- Python 3.x
- Scrapy
- Internet connection

**Installation:**
1. Clone or download the repository to your local machine.
2. Install Scrapy and other dependencies by running `pip install -r requirements.txt`.
3. Customize the scraper settings and parameters in the `settings.py` file according to your preferences.
4. Specify the list of websites to be scanned in the input file or directly within the scraper code.
5. Run the scraper using the command `scrapy crawl contact-info`.

**Usage:**
1. Configure the desired scraping parameters such as website list and proxy settings in the `settings.py` file.
2. Run the scraper using the command `scrapy crawl contact-info`.
3. Monitor the scraping process and wait for it to complete.
4. Once the scraping is finished, the collected contact information, CMS details, and social media links will be available for further analysis or integration.

**Contributing:**
Contributions to the project are welcome! Feel free to fork the repository, make improvements, and submit pull requests.

**Disclaimer:**
Please use this tool responsibly and ensure compliance with website terms of service, privacy policies, and any applicable laws and regulations regarding web scraping and data usage.

**License:**
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
