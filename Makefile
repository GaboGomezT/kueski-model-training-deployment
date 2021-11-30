build:
	docker build -t model-training .

run:
	docker run -v ~/.aws/credentials:/root/.aws/credentials --env-file ./.env -it model-training