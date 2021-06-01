# cryptoprices

Simple full stack web app that takes user's crypto amount and returns USD value.  Requires the following GCP Services:

1. Cloud Scheduler (write to Pubsub once every 10 minutes) to trigger...
2. Cloud Function (leveraging Secret Manager) to download pricing data as json file and store in...
3. Cloud Storage
4. App Engine (front end/back end code)

With low usage this probably costs ~$15-20/mo but YMMV :)

More info at: https://snoozesecurity.blogspot.com/2021/06/my-first-full-stack-web-app-and-of.html