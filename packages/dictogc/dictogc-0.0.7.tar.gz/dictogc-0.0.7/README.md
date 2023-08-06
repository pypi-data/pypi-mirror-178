# Description
This command line tool sync dipendentincloud.it timesheet with google calendar

# Install

- cd
- python -m venv .venv_dictogc
- source .venv_dictogc/bin/activate
- pip install --upgrade dictogc
- run dictogc
- nano xxx.ini *insert email, password and client_id of dipendenti in cloud*
- configure GCP, download your client_secret.json (OAuth) and copy this (for example) on ~/.config/dictogc/google_credentials.json (ref: https://google-calendar-simple-api.readthedocs.io/en/latest/getting_started.html#credentials)
- re-run dictogc
- enjoy result
- now you can add to gnome top panel using executor extension and set to run script every hour: .venv_dictogc/bin/dictogc