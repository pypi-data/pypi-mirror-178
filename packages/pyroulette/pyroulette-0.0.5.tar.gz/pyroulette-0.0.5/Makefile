build: clean lint test
	python -m build --sdist --wheel -n

clean:
	rm -rf build/ dist/ *.egg-info/ .eggs/ .pytest_cache/ .mypy_cache/ .coverage */__pycache__/ __pycache__/

publish: build
	twine upload dist/*

lint:
	isort --profile black .
	black .
	flake8 --max-line-length=88 --extend-ignore=E203,W503 pyroulette/

test:  # TODO: replace with real tests
	python app.py && python strategy.py

serve:
	python -m http.server 1337

demo:
	scp -P 10044 index.html git@mlden.com:/data/f/play.html
	@echo "visit http://clfx.cc/play.html"

.PHONY: build publish clean lint test
