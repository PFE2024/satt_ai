# AI Influencer Analysis

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This project introduces an AI model designed to aid in verifying the compliance of influencer publications, detecting whether influencer accounts are bots, and analyzing influencer communities. The model focuses on two popular social media platforms, Twitter and TikTok. It offers services in the form of an API for analysis most importent ones are: user verification, followers/following analysis of Twitter accounts, and publication compliance analysis based on brand campaign guidelines.

## Features and Functionality

- **User Verification Service:** This service allows users to verify the authenticity of an influencer on Twitter or TikTok. By providing the influencer's username, access token, and oracle type (Twitter or TikTok), the AI model analyzes various parameters to determine if the account is operated by a human or a bot
- **Change prediction Service:** allowing users to modify AI results.
- **Retrain model Service:** train AI model after humain verification to improve accuracy,this server trains the models every day at 8 AM.

- **Followers/Following Analysis Service:** This service provides users with the ability to assess the authenticity and quality of an influencer's followers and following on Twitter. By supplying the influencer's username and oracle type, the AI model evaluates the genuineness of their social connections.

- **Publication conformity Service:** This service helps analyze the conformity of influencer publications to the campaign guidelines provided by brand partners. By inputting the influencer's post ID, the specific campaign requirements, and oracle type, the AI model evaluates the alignment between the content and the brand's objectives. 
- **Check all Service:** This service help to make a global score for influencer according to his User Verification score and publications conformity score.
**Please note** that the output of these APIs is a score ranging from 1 to 5.
## Usage

Before using our project, please follow the steps below:

1. Fill in the `.env` file with the necessary credentials and configuration.

2. Install the required dependencies and libraries. You can use the command `pip3 install -r requirements.txt` to install them if you want only the final result or use the command `pip install -r requirements2_venv.txt` if you want to use our full project.
3. Run the following commands to download the necessary resources:
```bash
RUN python3 -m spacy download en_core_web_sm
RUN python3 -c "import nltk; nltk.download('punkt')"
RUN python3 -c "import nltk; nltk.download('averaged_perceptron_tagger')"
python3 -m nltk.downloader stopwords 
```
To utilize this AI model and its services, follow the steps below:

1. Import the AI model and relevant functions into your codebase.

2. Run the appropriate service by executing:
   - For the "check_all" server port 8084:
   ```bash
   python wsgi.py 
   ```
   - For the "User Verification" server port 8080:
   ```bash
   python user_wsgi.py 
   ```
   - For the "Change prediction" server port 8085:
   ```bash
   python change_wsgi.py 
   ```
   - For the "retrain model" server:
   ```bash
   python run.py
   ```
   - For the "Followers/Following Analysis" server 8081:
   ```bash
   python fo_wsgi.py 
   ```
   - For the "Publication conformity" server 8082:
   ```bash
   python text_wsgi.py
   ```
3. Use the appropriate API service by calling the corresponding function and providing the required inputs.

4. Retrieve the output from the API, which will provide the desired analysis and scores.

## Directory Structure
The project directory structure is organized as follows:
- `modelAI\resultat_finale`: Contains the research results and resources.
- `twitter`: Contains files and resources related to Twitter analysis.
- `tiktok`: Contains files and resources related to TikTok analysis.
- `posts_confirm`: Contains files and resources related to post confirmation analysis.
## Disclaimer

While this AI model aims to provide accurate assessments, it is important to note that it may not be infallible. False positives and false negatives may occur. Therefore, it is advisable to use the results as a reference rather than a definitive judgment.

## Code Example

### Here is an example of how to use
### Check user API:
![check_twitter_user](https://github.com/PFE2024/satt_ai/assets/96917892/e3899dad-e22f-49e5-9117-e03160c3fb7c)
### Check followers API:
![check_followers](https://github.com/PFE2024/satt_ai/assets/96917892/b8a518d4-6156-48eb-bcfc-872508b28050)
### Check following API:
![check_following](https://github.com/PFE2024/satt_ai/assets/96917892/3e2198e9-e975-426a-ac58-4fa52f756dd0)
### Change prediction API:
![change_tiktok](https://github.com/PFE2024/satt_ai/assets/96917892/ac322af1-739e-4dd9-b1be-f55f2792bc58)
### Post confirm twitter:
![twitter_text](https://github.com/PFE2024/satt_ai/assets/96917892/8c0e7d3e-74e0-419a-a291-b732a4a4d2bc)
### Post confirm tiktok:
![tiktok_text](https://github.com/PFE2024/satt_ai/assets/96917892/2b42a603-3f0f-441a-a779-39df969c8c12)

## Acknowledgments
We would like to express our sincere gratitude to our academic institution, ISET Bizerte, for their invaluable contributions to the development of this project. Their support and guidance have been instrumental in its success.
We would also like to extend our appreciation to the BrosTechnologie team for their continuous support and valuable feedback throughout the entire lifecycle of the project. Their input has greatly contributed to its improvement and overall quality.
