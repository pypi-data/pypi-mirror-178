import datetime
import requests
from dateutil.relativedelta import relativedelta
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
import logging
import os
import sys
import configparser
import appdirs


CONFIG_FILE = 'dictogc.ini'
DIC_BASE_URL = 'https://secure.dipendentincloud.it/backend_apiV2'

logging.basicConfig(filename='/tmp/dictogc.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('dictogc')


def config():
    cfg = configparser.ConfigParser()
    if sys.platform == 'linux':
        os.environ['XDG_CONFIG_DIRS'] = '/etc:/usr/local/etc'
    cfg_dirs = appdirs.site_config_dir('dictogc', multipath=True).split(':')
    cfg_dirs.append(appdirs.user_config_dir('dictogc'))
    cfg_dirs.append(os.path.dirname(os.path.abspath(__file__)))
    cfg_dirs.reverse()
    for d in cfg_dirs:
        cfg_file_path = os.path.join(d, CONFIG_FILE)
        cfg.read(cfg_file_path)
        if 'dipendentincloud.it' in cfg:
            email = cfg['dipendentincloud.it']['email']
            password = cfg['dipendentincloud.it']['password']
            client_id = cfg['dipendentincloud.it']['client_id']
            if email == '<INSERT_EMAIL>' or password == '<INSERT_PASSWORD>' or client_id == '<INSERT_CLIENT_ID>':
                print(f'insert your credentials in {cfg_file_path}')
                return
            return email, password, client_id, d
    else:
        cfg_file_path = os.path.join(appdirs.user_config_dir('dictogc'), CONFIG_FILE)
        try:
            cfg['dipendentincloud.it'] = {
                'email': '<INSERT_EMAIL>',
                'password': '<INSERT_PASSWORD>',
                'client_id': '<INSERT_CLIENT_ID>'
            }
            if not os.path.exists(cfg_file_path):
                os.makedirs(os.path.dirname(cfg_file_path))
            with open(cfg_file_path, 'w') as configfile:
                cfg.write(configfile)
            print(f"config auto created on {cfg_file_path}")
        except Exception as e:
            print(f"failed config read, error '{str(e)}' to auto-create empty config: {cfg_file_path}")


def main():
    try:
        cfg = config()
        if not cfg:
            exit(-1)
        email, password, client_id, config_dir = cfg
        now = datetime.datetime.now()
        gc = GoogleCalendar(credentials_path=os.path.join(config_dir, 'google_credentials.json'))
        session = requests.session()
        resp = session.post(f'{DIC_BASE_URL}/auth/login',
                            json={"data": None,
                                  "email": email,
                                  "password": password,
                                  "client_id": client_id})
        access_token = resp.json()['data']['access_token']
        resp_user = session.get(f'{DIC_BASE_URL}/user/login?flat=1',
                                headers={'authorization': access_token})
        resp_device = session.post(f'{DIC_BASE_URL}/devices/register_device', json={
            "data": None, "os": "Linux", "browser": "Chrome"
        })
        device_id = resp_device.json()['data']['device_id']
        access_token_user = resp_user.json()['data']['companies'][0]['access_token']
        person_id = resp_user.json()['data']['person']['id']
        resp_employee = session.get(f'{DIC_BASE_URL}/employees/flat', params={'active': 1, 'permission': 'timesheet_read'},
                                    headers={'authorization': access_token_user})
        employee_id = next(emp for emp in resp_employee.json()['data'] if emp['person_id'] == person_id)['id']
        resp_timesheet = session.get(f'{DIC_BASE_URL}/timesheet', params={
            'version': 2,
            'date_from': now.isoformat()[:10],
            'date_to': (now + relativedelta(months=6)).isoformat()[:10],
            'employees': employee_id
        }, headers={'authorization': access_token_user,
                    'accept': 'application/json', 'x-device-id': device_id})
        timesheet_user = resp_timesheet.json()['data']['timesheet'][str(employee_id)]
        for day in timesheet_user.keys():
            reasons = timesheet_user[day].get('reasons')
            if reasons:
                for reason in reasons:
                    name = reason['reason']['name']
                    for shift in reason['shifts']:
                        if shift['status'] == 'approved':
                            datetime_start_event = datetime.datetime.fromisoformat(f"{day}T{shift['time_start']}")
                            datetime_end_event = datetime.datetime.fromisoformat(f"{day}T{shift['time_end']}")
                            # create event isn't exist
                            gen_events = gc.get_events(time_min=datetime_start_event,
                                                       time_max=datetime_end_event,
                                                       order_by='startTime',
                                                       single_events=True,
                                                       query=name)
                            events = list(filter(lambda ev: bool(ev.start), gen_events))
                            if not events:
                                event = Event(name, start=datetime_start_event, end=datetime_end_event)
                                gc.add_event(event)
                                logger.info(f'event created: {str(event)}')
                            # decline all others event
                            gen_all_events = gc.get_events(time_min=datetime_start_event, time_max=datetime_end_event)
                            other_events = list(filter(lambda ev: ev.start and
                                                                  ev.start.date() == datetime_start_event.date() and
                                                                  ev not in events, gen_all_events))
                            if other_events:
                                for oev in other_events:
                                    if oev.attendees:
                                        attendee = next(att for att in oev.attendees if att.email == email)
                                        if attendee and attendee.response_status != 'declined':
                                            attendee.response_status = 'declined'
                                            gc.update_event(oev)
                                            logger.info(f'event declined: {str(oev)}')
        print('dictogc: done')
    except Exception as e:
        logger.exception(e)
        print('dictogc: failed')


if __name__ == "__main__":
    main()
