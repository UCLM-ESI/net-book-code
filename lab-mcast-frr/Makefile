
up: build
	docker compose up --remove-orphans -d
	sudo ./rm-bridge-addrs.sh
	sudo ./setup-hosts.sh

down:
	docker compose down

restart: down up

build:
	docker build -t lab2-router router
	docker compose build

clean: down
	-docker rmi lab2-router lab2-server
	-docker network prune -f

pim: restart
	./setup-static.sh
	./setup-pim.sh
