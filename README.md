# kueski-model-training-deployment
This repo contains the code necessary to train and save the persisted model to S3

### Steps to run locally and interact with AWS
1. Copy the `sample.env` to a `.env` file
2. Create a bucket named `kueski-ml-system` in S3
3. Configure aws-cli in your host machine (your user must have PUT and READ permissions in S3)
4. Run `make build`
5. Run `make run`
