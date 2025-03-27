
up:
	docker compose up --remove-orphans -d
	sudo ./rm-bridge-addrs.sh
	sudo ./setup-hosts.sh

down:
	docker compose down

restart: down build up

build:
	docker build -t lab2-router router
	docker compose build

clean: down
	-docker rmi lab2-router lab2-server
	-docker network prune -f

static: restart
	./setup-static.sh

.PHONY: rip
rip: restart
	./setup-rip.sh

ospf: restart
	./setup-ospf.sh

eigrp: restart
	./setup-eigrp.sh
