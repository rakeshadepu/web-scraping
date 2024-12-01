# Nailib Scraper for IB Math AI SL IA and EE Samples

## Objective
This project aims to scrape Sample IA's (Internal Assessments) and EE's (Extended Essays) from the **Nailib** website, 
focusing on IB Math AI SL samples. The extracted data will be structured, cleaned, and stored in **MongoDB** for each run, preventing duplication. 

### Key Data Points to Extract:
- **Title**: The name of the IA or EE.
- **Subject**: Example: Math AI SL.
- **Description**: Instructions, checklists, or summaries.
- **Sections**: Various sections within the IA/EE, like:
  - Introduction Guidance
  - Mathematical Information Usage
  - Mathematical Processes Applied
  - Interpretation of Findings
  - Validity and Limitations
  - Academic Honesty Guidelines
- **File Link**: Link to any downloadable resources, if available.
- **Word Count**: Extract word count from the page.
- **Time Estimate**: Estimated reading time (e.g., "11 mins read").
- **Checklist Items**: Subheadings or bullet points with guidelines.
- **Publication Date**: If available, extract the publication date.

## Task Breakdown

### Step 1: Website Exploration & Data Points Identification
- Navigate through the Nailib website, particularly the IB Math AI SL sample pages, to identify and extract the data points mentioned above.

### Step 2: Scraping & Data Cleaning
- Ensure proper structured extraction of data from the website.
- Clean the extracted data:
  - Normalize text fields (remove unnecessary whitespace).
  - Handle missing fields gracefully (e.g., when data points are not available on a page).
  - Handle inconsistencies like formatting issues.

### Step 3: MongoDB Integration
- Design a MongoDB schema to store IA/EE data:
  ```json
  {
    "title": "Sample IA Title",
    "subject": "Math AI SL",
    "description": "Checklist for IA",
    "sections": {
      # Content here processed in different sections based on headings
    },
    "word_count": 2112,
    "read_time": "11 mins",
    "file_link": "https://nailib.com/resource.pdf",
    "publication_date": "YYYY-MM-DD"
  }
  ```
- Implement MongoDB’s **upsert** functionality to prevent duplicate data storage.

### Step 4: Automation (Bonus)
- Implement automation using a scheduler like **Cron** to periodically scrape new data.
- Create a **REST API** for querying MongoDB to retrieve stored data.
- **Dockerize** the solution for portability and easy deployment.

## Technical Requirements
- **Language**: Python
- **Libraries**:
  - Scraping: `BeautifulSoup`, `Scrapy`, or `Selenium` for web scraping.
  - Database: `PyMongo` for MongoDB integration.
  - Error Handling: Implement robust error handling for network issues, missing data, etc.
  
## Evaluation Criteria
- **Data Accuracy (30%)**: Correct and structured extraction and cleaning of data.
- **Code Quality (25%)**: Clean, efficient, and well-documented code.
- **MongoDB Integration (20%)**: Proper design of MongoDB schema, upsert functionality, and efficient data querying.
- **Handling Edge Cases (15%)**: Graceful handling of missing or incomplete data.
- **Presentation (10%)**: Clear and concise documentation with code shared on a GitHub repository.

## How to Run the Scraper

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/nailib-scraper.git
   cd nailib-scraper
   ```

2. **Install Dependencies**:
   You can use `pip` to install the required dependencies.
   pip install -r requirements.txt
  
3. **Configure MongoDB**:
   - Ensure you have MongoDB running locally or use a cloud MongoDB instance.
   - Update the MongoDB URI in `scrapper.py` with your connection details.

4. **Run the Scraper**:
   - Execute the script to start scraping.
   
   python scrapper.py

5. **View Data in MongoDB**:
   After running the script, the data will be stored in the MongoDB collection `sample_data`. You can use a MongoDB client or MongoDB's web interface (e.g., MongoDB Atlas) to view the data.

## Bonus Features (Optional)

- **Automate the Scraper**: Set up a **cron job** to run the scraper at regular intervals to keep the data updated.
- **REST API**: Implement a simple REST API using Flask or FastAPI that allows users to query the stored IA/EE data from MongoDB.
- **Dockerize the Solution**: Create a `Dockerfile` and `docker-compose.yml` for easy containerization of the solution.

## Contribution

- Fork the repository and create a pull request for improvements or bug fixes.
- If you encounter any issues, feel free to open an issue on the GitHub repository.

## License

This project is open-source and available under the [MIT License](LICENSE).
