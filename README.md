# local_rewards_platform

docker-compose run web python manage.py makemigrations

docker-compose run web python manage.py migrate

docker-compose run web python manage.py createsuperuser

run web python manage.py seed_reward_types
run web python manage.py seed_reward_categories
docker-compose run web python manage.py seed_reward_brands


docker-compose run web python import_rewards.py