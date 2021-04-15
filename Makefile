.PHONY: mypy
mypy:
	docker exec -it koop-backend mypy .
