.PHONY: setup_db
setup_db:
	docker build -t onlinetest_db_api:test . && docker run -d -p 8080:8080 onlinetest_db_api:test



.PHONY: test
test:
	poetry run python -m unittest