build:
	docker build . -t openai-agent-sdk-devin

exec:
	docker run -it --rm \
		-v $(shell pwd):/app \
		--env-file .env \
		openai-agent-sdk-devin \
		bash