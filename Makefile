# Variables
VENV_NAME=venv
PYTHON=$(VENV_NAME)/Scripts/python.exe
PIP=$(VENV_NAME)/Scripts/pip.exe

# Create virtual environment  install --upgrade pip
init:
	python -m venv $(VENV_NAME)
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

# Run FastAPI app locally
run:
	$(PYTHON) -m uvicorn app.main:app --reload

# Freeze dependencies
freeze:
	$(PIP) freeze > requirements.txt

# Format code with black
format:
	$(PIP) install black
	$(VENV_NAME)/bin/black app/

# Run tests (if you add pytest later)
test:
	$(PIP) install pytest
	$(VENV_NAME)/bin/pytest tests/

# Docker build and run
docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

# Clean up
clean:
	rm -rf $(VENV_NAME) __pycache__ .pytest_cache




# make init         # Set up virtualenv and install dependencies
# make run          # Start FastAPI locally
# make freeze       # Save current dependencies
# make docker-up    # Build and run with Docker
# make docker-down  # Stop containers
# make clean        # Remove venv and cache

#/