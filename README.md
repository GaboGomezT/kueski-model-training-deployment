# kueski-model-training-deployment
This repo contains the code necessary to train and save the persisted model to S3

### Steps to run locally
1. Download the Feature Parquet
2. Build the image with `docker build -t model-training .`
3. Run the container with the following command `docker run -v ~/.aws/credentials:/root/.aws/credentials  -it -v "$(pwd)":/src model-training bash`
4. Inside the container simply run `python main.py`

### Steps to run locally and interact with AWS
1. Create a bucket named `kueski-ml-system` in S3
2. Configure aws-cli in your host machine (your user must have PUT and READ permissions in S3)
3. Build the image with `docker build -t model-training .`
4. Run the container with the following command `docker run -v ~/.aws/credentials:/root/.aws/credentials  -it -v "$(pwd)":/src model-training bash`
5. Inside the container run the following command `export STAGE=prod`
4. Inside the container simply run `python main.py`
