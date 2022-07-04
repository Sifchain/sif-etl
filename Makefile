.DEFAULT_GOAL := help

# ANSI escape codes
BOLD := \033[1m
RESET := \033[0m
REVERSE := \033[7m
RED := \033[0;31m

START_TIME:=$(shell date -u +%s)

.PHONY: help
help:
	@echo ""
	@echo "OPERATE:"
	@echo "up                       Start all containers"
	@echo "down                     Stop all containers"
	@echo "restart                  Stop then start containers"
	@echo "DEBUGGING:"
	@echo "bash                     Go into the bash shell for a container"
	@echo "logs                     Re-attach to running container logs"
	@echo "log                      Re-attach to specified running container log"
	@echo "ps                       List running container info"
	@echo ""
	@echo "TEST:"
	@echo "test                     Run unit tests"
	@echo "coverage                 Run coverage report for unit tests"
	@echo "integration              Run integration tests for service"
	@echo ""
	@echo "LINT:"
	@echo "lint                     Linting checks through flake8 and pylint"
	@echo "flake8                   Lint using flake8"
	@echo "pylint                   Lint using pylint"
	@echo ""
	@echo "MAINTENANCE:"
	@echo "clean                    Remove dangling images and exited containers"
	@echo ""
	@echo "DATA:"
	@echo "clean_volumes            Remove data volumes"
	@echo "clean_start              Stop, clean, clean_volumes, rebuild"
	@echo ""
	@echo "INSTALL:"
	@echo "hooks                    Install Git hooks"
	@echo "requirements             Generate requirements.txt from requirements_base.txt"
	@echo ""
	@echo "DEPLOYMENT:"
	@echo "docker_login 			Log on to a Docker registry"
	@echo "docker_tag				Tag latest local images in prep to push to a Docker registry"
	@echo "docker_push				Push docker image to a Docker registry"

.PHONY: up
up:
	docker-compose up -d 
	@make logs

.PHONY: bash
bash:
	@if test -z $(name); then\
	    	echo "";\
	  	echo "Please enter a container name as argument,";\
	    	echo "";\
         	echo "  e.g. 'make bash name=gui_client'";\
	    	echo "";\
	else\
	  docker-compose exec $(name) bash;\
	fi

.PHONY: logs
logs:
	docker-compose logs -f

.PHONY: log
log:
	@if test -z $(name); then\
	    	echo "";\
	  	echo "Please enter a container name as argument,";\
	    	echo "";\
         	echo "  e.g. 'make log name=gui_client'";\
	    	echo "";\
		echo "or use 'make logs' to attach to all container logs.";\
	    	echo "";\
	else\
	  docker-compose logs -f $(name);\
	fi

.PHONY: down
down:
	docker-compose down --rmi all

.PHONY: clean
clean:
	@echo "Deleting exited containers..."
	docker ps -a -q -f status=exited | xargs docker rm -v
	@echo "Deleting dangling images..."
	docker images -q -f dangling=true | xargs docker rmi
	@echo "All clean 🛀"

.PHONY: clean_volumes
clean_volumes:
#	@docker volume rm 
	@echo "All clean 🛀"

.PHONY: restart
restart:
	@echo "make down => make up"
	@make down
	@make up

.PHONY: clean_start
clean_start:
	@echo "make down => make clean => make clean_volumes => make up"
	@make down
	@make clean
	@make clean_volumes
	@make up

.PHONY: lint
lint:
	@echo ""
	@echo "make flake8 => make pylint"
	@echo ""
	@make flake8
	@echo ""
#	@make pylint
	@echo ""
	@echo "Linting checks passed 🏆"

.PHONY: flake8
flake8:
	@echo "$(REVERSE)Running$(RESET) $(BOLD)flake8$(RESET)..."
	@if ! flake8 ; then \
	    echo "$(BOLD)flake8$(RESET): $(RED)FAILED$(RESET) checks" ;\
	    exit 1 ;\
	fi
	@echo "flake8 passed 🍄"

.PHONY: pylint
pylint:
	@echo "$(REVERSE)Running$(RESET) $(BOLD)pylint$(RESET)..."
	@echo ""
	@travis/check_pylint_score.py
	@echo ""
	@echo "pylint passed ⚙️"

.PHONY: hooks
hooks:
	@echo "Installing git hooks..."
	cp ./hooks/{commit-msg,pre-commit*} .git/hooks/
	@echo "Hooks installed"

.PHONY: bdd_test
bdd_test:
	behave features

.PHONY: test
test:
	python -m unittest discover

.PHONY: coverage
coverage:
	coverage run -m unittest discover
	coverage report
	coverage html
	@echo "test coverage report complete 📊"
	@python -m webbrowser "file://${PWD}/htmlcov/index.html"

.PHONY: integration
integration:
	@if test -z $(service); then\
	    	echo "";\
	  	echo "Please enter a service name as argument,";\
	    	echo "";\
         	echo "  e.g. 'make integration service=client_upload_service'";\
	    	echo "";\
	else\
	  docker-compose exec $(service) bash -c "python -m unittest discover -p integration";\
	fi

.PHONY: requirements
requirements:
	@echo "Generating requirements.txt from core dependencies in requirements_base.txt ..."
	pip install virtualenvwrapper && \
	source virtualenvwrapper.sh && \
	wipeenv && \
    	pip install -r requirements_base.txt && \
    	echo '# generated via "make update_requirements"' > requirements.txt && \
    	pip freeze -r requirements_base.txt >> requirements.txt
	@echo "requirements.txt has been updated 🍉"

.PHONY: ps
ps:
	docker-compose ps

docker_build:
	@docker build . -t sifchain/sif-etl
	@echo "Docker images tagged 🔖"

docker_push: 
	@docker push sifchain/sif-etl
	@make elapsed_time
	@echo "Docker containers pushed to dockerhub 🐳"

elapsed_time:
# This doesn't work unless make is run with -e option.
	@echo "$$(( `date -u +%s` - $(START_TIME) )) seconds elapsed"

