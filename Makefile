all: build

build:
	docker build -t chess-agent .

run: build
	docker run -it chess-agent