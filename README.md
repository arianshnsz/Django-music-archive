# Django music archive
A simple Django project that lets you organize your music and audio files.
You can Create Albums and assign songs to them.

## Features
  Storing, Managing, and Playing songs.
  Playing songs locally. You can use this project on a Raspberry Pi and use it as a media player
## How to run

1. Make sure `python3` and `pip` are installed in your system.
2. clone the project and make the development environment ready:

```bash
git clone https://github.com/arianshnsz/Django-Task-Reminder.git
python -m venv .venv # Create a virtual environment called .venv
source .venv/bin/activate # activate the virtual environment
pip install -r requirements.txt # install the required packages
```
<details>

<summary> 
3. Generate the Django Secrete key (click to show the steps): 
</summary>

   * Access the Python Interactive Shell:
   
   ```bash
   django-admin shell
   ```
   
   * Import the `get_random_secret_key()` function from `django.core.management.utils`:
   
   ```bash
   from django.core.management.utils import get_random_secret_key
   ```
   
   * Generate the Secrete key using `get_random_secret_key()` function:
   
   ```bash
   get_random_secret_key()
   ```
   
   * In the existing directory, create a file name `.env` and paste the following line inside it:
   
   ```
   SECRET_KEY = "... paste your generated secret key ..."
   ```
</details>

4. Create database tables:
```bash
python manage.py migrate
```
5. Run the project and visit the following website.
```bash
python manage.py runserver
```
