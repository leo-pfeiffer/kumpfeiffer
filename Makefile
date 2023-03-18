.PHONY: compilemessages
# Compile the locale
compilemessages:
	python manage.py compilemessages -l de -i venv

.PHONY: makemessages
# Create the locale
makemessages:
	python manage.py makemessages -l de -i venv

.PHONY: locale
# Compile and create the locale
locale:
	make compilemessages
	make makemessages

.PHONY: help
# Found here: https://stackoverflow.com/a/35730928/12168211
# Print available commands
help:
	@echo "=============================================================="
	@echo "Available Make commands ======================================"
	@echo "=============================================================="
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t