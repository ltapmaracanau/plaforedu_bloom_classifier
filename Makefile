all: build

build:
	docker build -t bloom_classifier .

run:
	docker run -p 5000:5000 --name bloom_classifier -it bloom_classifier

stop:
	docker stop bloom_classifier

clean:
	docker rm bloom_classifier

logs:
	docker logs bloom_classifier
