
up:
	docker build -t router router
	docker compose up --remove-orphans -d

down:
	docker compose down

restart: down build up

build:
	docker compose build
