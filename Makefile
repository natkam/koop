.PHONY: mypy
mypy:
	docker exec -it koop-backend mypy .

.PHONY: test
test:
	docker exec -it koop-backend python manage.py test
