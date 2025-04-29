# local_rewards_platform
docker-compose up --build 

docker-compose run web python manage.py makemigrations

docker-compose run web python manage.py migrate

docker-compose run web python manage.py createsuperuser

docker-compose run web python import_rewards.py