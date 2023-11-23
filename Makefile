build:
	docker build -t bash_gpt .

run:
	docker run -it -p 4000:80 bash_gpt

test:
	docker run -it bash_gpt pytest