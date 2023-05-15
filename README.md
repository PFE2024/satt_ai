# AI Influencer Analysis

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This project introduces an AI model designed to aid in verifying the compliance of influencer publications, detecting whether influencer accounts are bots, and analyzing influencer communities. The model focuses on two popular social media platforms, Twitter and TikTok. It offers three distinct services in the form of an API for analysis: user verification, followers/following analysis of Twitter accounts, and publication compliance analysis based on brand campaign guidelines.

## Features and Functionality

- **User Verification Service:** This service allows users to verify the authenticity of an influencer on Twitter or TikTok. By providing the influencer's username, access token, and oracle type (Twitter or TikTok), the AI model analyzes various parameters to determine if the account is operated by a human or a bot. Additionally, this service provides a change prediction API, allowing users to modify AI results and then retrain the model using the rerun API to improve accuracy.

- **Followers/Following Analysis Service:** This service provides users with the ability to assess the authenticity and quality of an influencer's followers and following on Twitter. By supplying the influencer's username and oracle type, the AI model evaluates the genuineness of their social connections.

- **Publication Compliance Analysis Service:** This service helps analyze the conformity of influencer publications to the campaign guidelines provided by brand partners. By inputting the influencer's post ID, the specific campaign requirements, and oracle type, the AI model evaluates the alignment between the content and the brand's objectives. Please note that the output of these APIs is a score ranging from 1 to 5.

## Usage

Before using our project, please follow the steps below:

1. Fill in the `.env` file with the necessary credentials and configuration.

2. Install the required dependencies and libraries as specified in the project documentation. You can use the command `pip3 install -r requirements.txt` to install them.

To utilize this AI model and its services, follow the steps below:

1. Import the AI model and relevant functions into your codebase.

2. Run the appropriate service by executing `python wsgi.py` for the User Verification Service or `python fo_wsgi.py` for the Followers/Following Analysis Service.

3. Use the appropriate API service by calling the corresponding function and providing the required inputs.

4. Retrieve the output from the API, which will provide the desired analysis and scores.

## Directory Structure

The results of our research can be found in the `modelai` folder. Additionally, our work is organized into three separate directories: `twitter`, `tiktok`, and `posts_confirm`. Each directory contains relevant files and resources for the respective analysis.

## Disclaimer

While this AI model aims to provide accurate assessments, it is important to note that it may not be infallible. False positives and false negatives may occur. Therefore, it is advisable to use the results as a reference rather than a definitive judgment.

## Code Example

### Here is an example of how to use
### check user API:
![image](https://github.com/PFE2024/satt_ai/assets/96917892/b846a068-ada2-4a49-a78e-73fb34387d1e)
### check followers API:
![image](https://github.com/PFE2024/satt_ai/assets/96917892/f9090c8f-9832-488f-8cf2-20d6a62bd783)
## Acknowledgments
We would like to express our sincere gratitude to our academic institution, ISET Bizerte, for their invaluable contributions to the development of this project. Their support and guidance have been instrumental in its success.

We would also like to extend our appreciation to the BrosTechnologie team for their continuous support and valuable feedback throughout the entire lifecycle of the project. Their input has greatly contributed to its improvement and overall quality.
