from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
print(f"Your new SECRET_KEY is: {secret_key}")
