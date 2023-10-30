from datetime import datetime, timezone

#note for contributors: this should always be set to a couple minutes in the future when pushing
#there is a pre-commit hook that will do this for you, see end of README.md
VERSION_DATE = datetime(2023, 10, 30, 19, 38, 6, tzinfo=timezone.utc)