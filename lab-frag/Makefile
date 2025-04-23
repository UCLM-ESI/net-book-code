
up: build
	docker compose up --remove-orphans -d
	sudo ./rm-bridge-addrs.sh
	sudo ./setup-routing.sh

down:
	docker compose down

restart: down build up

build:
	docker compose build router
	docker compose build

clean: down
	docker rmi router server
