#!/bin/zsh

heroku_push() {
  git push heroku main
}

heroku_set_config() {
  heroku config:set "$1"="$2"
}

heroku_unset_config() {
  heroku config:unset "$1"
}

heroku_manage() {
  heroku run python manage.py "$1"
}
