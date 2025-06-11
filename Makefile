SHELL := bash
.SHELLFLAGS = -e -o pipefail -c
.DEFAULT_GOAL := help
.NOTPARALLEL:
.SILENT: # use set -v to print commands executed
.ONESHELL:
# This Makefile is used as a script runner, rather than a build system
.PHONY: $(MAKECMDGOALS)
MAKEFLAGS += --no-print-directory

install: ## Install hooks
	cd ./.git/hooks
	for hook in post-checkout post-merge post-rebase; do
	    ln -s -f ../../netlinks.py ${hook}
	done
	echo "Installed git hooks in .git/hooks:"
	ls -1 .

help: ## Display this help
	awk '
	  BEGIN { FS = ":.*##"; printf "Usage:\n  make \033[36m<target>\033[0m\n" }
	  /^[a-zA-Z_\/-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }
	  /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } 
	  ' $(MAKEFILE_LIST)
