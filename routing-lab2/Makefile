
up:
	docker build -t router router
	docker compose up --remove-orphans -d

down:
	docker compose down

restart: down build up

build:
	docker compose build

clean: down
	docker rmi router server

static: restart
	sudo ./fix-bridge-addrs.sh
	./setup-static.sh

.PHONY: rip
rip: restart
	sudo ./fix-bridge-addrs.sh
	./setup-rip.sh

ospf: restart
	sudo ./fix-bridge-addrs.sh
	./setup-ospf.sh
