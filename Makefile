process:
	./env/bin/python3 ./process.py

download:
	@./env/bin/python3 ./download.py

static:
	./env/bin/python3 ./create_static_site.py

crunk: setup env requirements check
	@echo
	@echo "Get crunk with it. Get loose with it."
	@echo

setup:
	sudo apt update
	sudo apt --fix-broken install -y
	sudo apt install -y fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcairo2 libcups2 libdrm2 libgbm1 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libu2f-udev libvulkan1 libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils
	wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O google-chrome-stable_current_amd64.deb
	sudo dpkg -i google-chrome-stable_current_amd64.deb

env:
	python3 -m venv ./env

requirements:
	@rm -rf ~/.cache/pip/selfcheck/
	./env/bin/pip install --quiet flake8 pylint black
	./env/bin/pip install --quiet --requirement requirements.txt

check:
	which git && git --version
	which node && node --version
	which npm && npm --version
	which npx && npx --version
	which google-chrome && google-chrome --version
	./env/bin/python3 --version
	./env/bin/pip --version
	./env/bin/flask --version
	./env/bin/black --version

lint:
	./env/bin/black --check *.py
	./env/bin/flake8 --ignore=E501  *.py
	./env/bin/pylint *.py

black:
	black *.py

clean:
	rm -f .*.swp
	rm -f google-chrome-stable_current_amd64.deb
	rm -rvf ./downloads

nuke: clean
	rm -rvf ./env
	rm -rvf ./public

debug:
	./env/bin/flask run --host 0.0.0.0 --port 3000 --debug

all: env requirements check lint download process static

.PHONY: all process download env requirements lint clean static
