
up:
	docker build -t router router
	docker compose up --remove-orphans -d
	sudo ./fix-bridge-addrs.sh

down:
	docker compose down

restart: down build up

build:
	docker compose build

clean: down
	docker rmi router server

static: restart
	./setup-static.sh

.PHONY: rip
rip: restart
	./setup-rip.sh

ospf: restart
	./setup-ospf.sh
