🚀 Serverless CRUD API with AWS Lambda, API Gateway & DynamoD

📌 Project Overview

This project is a fully serverless CRUD API built on AWS.
It helped me understand how to design a backend system without managing servers, using AWS managed services for compute, routing, database, and monitoring.

The goal was to practice serverless architecture and learn how different AWS services connect together in real-world projects.

🛠️ Tech Stack

AWS Lambda → runs Python code for all CRUD operations.

Amazon API Gateway → exposes Lambda as REST endpoints and handles routing.

Amazon DynamoDB → NoSQL database used to store the items.

Amazon CloudWatch → used for monitoring, debugging, and checking logs.

IAM (Identity and Access Management) → provided secure permissions so Lambda could access DynamoDB.

⚙️ Features

Create items in DynamoDB (POST).

Read items by ID or list all items (GET).

Update items with new data (PUT).

Delete items from the table (DELETE).

Log all executions in CloudWatch for debugging.

🐞 Errors I Faced & Fixes

Syntax errors in Lambda code

I had missing imports and indentation problems in Python.

Fixed them by carefully debugging the logs in CloudWatch.

DynamoDB access denied

My Lambda role didn’t have permission to write to DynamoDB.

Solved by attaching the AmazonDynamoDBFullAccess policy in IAM.

API Gateway returning 403/500 errors

The integration between API Gateway and Lambda was not correct.

Fixed by enabling Lambda Proxy Integration.

Data not saving correctly

My JSON body format was wrong.

Solved by sending a consistent structure:

{
  "id": "1",
  "name": "Test Item",
  "description": "This is a test"
}

📖 What I Learned

How Lambda, API Gateway, and DynamoDB work together to form a complete serverless backend.

The importance of IAM permissions when connecting AWS services.

How to debug real-world problems using CloudWatch logs.

That building cloud projects is not just about code but also about configurations and integrations.

🌍 Real-World Applications

This kind of serverless API can be used in:

User management systems (add/update/delete users).

IoT apps (store sensor data).

E-commerce apps (manage product catalogs).

Mobile/web backends that need scalable APIs without servers.

✨ Final Thoughts

This project gave me hands-on experience with AWS serverless services.
Even though I faced multiple errors, solving them helped me understand the core concepts of serverless development and gave me confidence in working with cloud services.
