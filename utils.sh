#!/bin/zsh

heroku_push() {
  git push -f heroku main
}

heroku_set_config() {
  heroku config:set "$1"="$2" -a kumpfeiffer
}

heroku_unset_config() {
  heroku config:unset "$1" -a kumpfeiffer
}

heroku_manage() {
  heroku run python manage.py "$1" -a kumpfeiffer
}

heroku_logs() {
  heroku logs --tail -a kumpfeiffer
}
