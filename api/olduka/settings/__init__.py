import os


current_environment = os.getenv('ENVIRONMENT_SETTINGS')

if current_environment == "PRODUCTION":
    from olduka.settings.production import *
elif current_environment == "DEVELOPMENT":
    from olduka.settings.development import *

