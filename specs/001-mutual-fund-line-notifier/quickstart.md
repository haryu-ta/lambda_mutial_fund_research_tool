# Quickstart: Mutual Fund LINE Notifier

## Prerequisites
- AWS CLI configured
- LINE Messaging API Channel Access Token & User ID
- Python 3.13 environment

## Local Development
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install beautifulsoup4 line-bot-sdk pytest
   ```
3. Set environment variables:
   ```bash
   export LINE_CHANNEL_ACCESS_TOKEN='your_token'
   export LINE_USER_ID='your_user_id'
   ```
4. Run tests:
   ```bash
   pytest
   ```

## Deployment (AWS Lambda)
1. Package the function with dependencies:
   ```bash
   mkdir package
   pip install --target ./package -r requirements.txt
   cd package
   zip -r ../deployment_package.zip .
   cd ..
   zip deployment_package.zip src/*.py
   ```
2. Upload `deployment_package.zip` to AWS Lambda.
3. Configure the handler as `src.lambda_function.lambda_handler`.
4. Configure environment variables in Lambda Console:
   - `LINE_CHANNEL_ACCESS_TOKEN`
   - `LINE_USER_ID`
5. Create an EventBridge rule with the following JSON input:
   ```json
   [
     {"id": "8931123C", "display_name": "Sample Fund"}
   ]
   ```
