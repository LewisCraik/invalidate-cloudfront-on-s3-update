# Invalidate CloundFront on S3 Update
An AWS Lambda function to trigger a CloudFront invalidation when an S3 bucket is updated. The goal was to have one function that would work for many S3 Bucket/CloudFront distribution pairs.

To achieve this, the Lambda function is notified by the S3 bucket when a file is changed. The details of the CloundFront distribution linked to the bucket is recoded as a tag in the bucket properties, which is read by the Lambda function.

This function is inspired by [this blog post by Miguel Ángel Nieto](https://blog.miguelangelnieto.net/posts/Automatic_Cloudfront_invalidation_with_Amazon_Lambda.html), which got me most of the way there, and [this blog post by Yago Nobre](https://medium.com/@yagonobre/automatically-invalidate-cloudfront-cache-for-site-hosted-on-s3-3c7818099868) which helped with the method for linking the S3 buckets and the Lambda function.

## How to use
To use the Lambda function, the function itself needs to be set up in the Lambda Management Console. Permissions are set in the IAM Management Console. The trigger and link to distribution are set up for each bucket in the S3 Management Console.

### Lambda Management Console
From the AWS Lambda Dashboard:
* Click to create a new function.
* Select "Author from scratch".
* Give your function a name e.g. "invalidateCloudFront".
* Select "Python 2.7" as your runtime.
* Under permissions, choose "Create a new role with basic Lambda permissions", this will be updated in a later step.
* Finally select "Create function"

You now have a basic Lambda function, with a lambda_function.py file in the editor. Replace the code in the editor with the code from the lambda_function.py file in this repository.

### IAM Management Console
The function requires permissions to write logs, read tags from the S3 bucket and of course, create an invalidation. These permissions are set in the IAM Management Console.

Under "Roles", you will find a role with the name of your Lambda function followed by "-role-" and some random characters, for example "invalidateCloudFront-role-jxa5yv87". Alternativly, if you scroll down the page for your function in the Lambda Management Console, you will see a section called "Execution role", which has a link to edit your function on the the IAM Console.

From the "Role" page:
* Click on the policy, which should be called something stating with "AWSLambdaBasicExecutionRole".
* Click the "Edit policy" button, then select the JSON tab.
* Replace the code with the code from the policy.json file in this repository.
* Click "Review policy", then "Save changes".

### S3
There are 2 steps to link each S3 bucket to the Lambda function, setting the tag for the distribution and triggering the function. These need to be set up for each S3 bucket you wish to use with the Lambda Function.

To set the tag for the distribution ID, from the S3 Management Console:
* Select the bucket you want to link with the Lambda function.
* Go to the "Properties" tab, then "Tags", under "Advanced settings".
* Add a tag.
* The "Key" must be exactly "distributionId", noting capitalisation, as this is what the Lambda function is looking for.
* The Value is the distribution ID, this can be found in the CloudFront Management Console and is usually a 13 character string.
* Click "Save".

To trigger the function each time a file in the bucket is updated:
* Go to "Events", which is also in "Advanced settings" under "Properties".
* Click "+ Add notification".
* Give your notification a name, such as "InvalidateCloudFront".
* Select "All object create events" and "All object delete events".
* Leave "Prefix" and "Suffix" blank.
* Select "Lambda function" from the "Send to" drop down.
* Select your function from the "Lambda" drop down.
* Press "Save".

If you go back to your function in the Lambda Management Console you should see that it now has an S3 trigger listed (you may need to refresh the page).

### Test your function
Now is time to test your function - add a file to the S3 bucket and after a few minutes you should be able to see evidence of your function working in the following places:
* The "Monitoring" tab on your function in the Lambda Management Console.
* You CloudWatch logs.
* An invalidation will be listed in the "Invalidations" tab for your distribution on the CloudFront Management Console.

## Author
**[Lewis Craik](http://lewiscraik.co.uk)**
