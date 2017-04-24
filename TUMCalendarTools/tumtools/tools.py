import re
from icalendar import Calendar, Event

def cleanup_description(description):
    """Removes all uninteresting stuff from the event description ``description``."""
    relevant_parts = []
    parts = description.split(';')
    for item in parts:
        item = item.strip()
        if item not in ['', 'fix', 'Abhaltung', 'geplant', 'Import']:
            relevant_parts.append(item.replace('\n', ' '))

    return '\n'.join(relevant_parts)

def cleanup_summary(summary):
    """Removes all uninteresting stuff from the event title ``summary``."""
    summary = summary.rsplit(',', 1)[0]

    lecture_type = summary[-2:]
    summary = summary[:-2]

    module_name = None
    if summary.find("(") >= 0:
        module_name = summary[summary.find("(")+1:summary.find(")")]
        module_name = module_name.replace('Modul', '').strip()

    summary = re.sub("[\(\[].*?[\)\]]", "", summary)
    summary = summary.replace('- Übung -', '')
    summary = summary.replace('- Vorlesung -', '')
    summary = summary.replace('- Zusatzübung -', '')
    summary = summary.replace('- Praktikum -', '')
    summary = summary.replace('Übung', '')
    summary = summary.strip()


    if lecture_type == 'VO':
        summary += " (Vorlesung)"
    elif lecture_type == 'UE':
        summary += " (Übung)"
    elif lecture_type == 'VU':
        summary += " (Vorlesung/Übung)"
    elif lecture_type == 'SE':
        summary += " (Seminar)"
    elif lecture_type == 'PR':
        summary += " (Praktikum)"
    elif lecture_type == 'WS':
        summary += " (Workshop)"
    elif lecture_type == 'FA':
        summary += " (Fachprüfung)"
    elif lecture_type == 'MP':
        summary += " (Modulprüfung)"
    else:
        summary += " #################("+lecture_type+")"

    return (summary, module_name)

def cleanup_location(location):
    location = re.sub("[\(\[].*?[\)\]]", "", location)

    if location.find(",") != -1:
        location = location[:location.find(",")].strip() + " ("+location[location.find(",")+1:].strip()+")"

    return location


def parse_event(component):
    event = TUMEvent()
    event.dt_start = component.get('DTSTART')
    event.dt_end = component.get('DTEND')
    event.dt_stamp = component.get('DTSTAMP')
    event.recurring_i = component.get('X-CO-RECURRINGID')
    event.status = component.get('STATUS')
    event.uid = component.get('UID')

    (summary, module_name) = cleanup_summary(component.get('SUMMARY'))
    description = cleanup_description(component.get('DESCRIPTION'))
    if description != '':
        if(module_name != None):
            description += "\n"+module_name
    elif(module_name != None):
        description = module_name

    event.summary = summary
    event.description = description
    event.add_location(cleanup_location(component.get('LOCATION')))
    return event

class TUMEvent:
    dt_start = ''
    dt_end = ''
    dt_stamp = ''
    recurring_i = ''
    uid = ''
    summary = ''
    description = ''
    location = ''
    status = ''

    def is_event(self, evt):
        if self.summary != evt.summary: return False
        if self.dt_start.dt != evt.dt_start.dt: return False
        if self.dt_end.dt != evt.dt_end.dt: return False
        return True

    def add_location(self, location):
        if self.location == '':
            self.location = location
        else:
            self.location += "\n"+location

    def gen_event(self):
        event = Event()
        event.add('DTSTART', self.dt_start)
        event.add('DTEND', self.dt_end)
        event.add('DTSTAMP', self.dt_stamp)
        event.add('X-CO-RECURRINGID', self.recurring_i)
        event['UID'] = self.uid
        event.add("DESCRIPTION", self.description)
        event.add('SUMMARY', self.summary)
        event.add('LOCATION', self.location)
        return event


def execute(content):
    gcal = Calendar.from_ical(content)


    ncal = Calendar()
    ncal.add('METHOD', gcal.get("METHOD"))
    ncal.add('VERSION', gcal.get("VERSION"))
    ncal.add('CALSCALE', gcal.get("CALSCALE"))
    ncal.add('X-WR-TIMEZONE', gcal.get("X-WR-TIMEZONE"))
    ncal.add('X-PUBLISHED-TTL', gcal.get("X-PUBLISHED-TTL"))
    ncal.add('PRODID', gcal.get("PRODID"))
    ncal.add('X-WR-CALNAME', gcal.get("X-WR-CALNAME"))
    ncal.add('X-WR-CALDESC', gcal.get("X-WR-CALDESC"))

    tum_events = []

    for component in gcal.walk():
        if component.name == "VEVENT":
            event = parse_event(component)

            duplicate_event = False
            for item in tum_events:
                if item.is_event(event):
                    duplicate_event = True
                    item.add_location(event.location)
                    break

            if not duplicate_event:
                tum_events.append(event)

    event_str = ''

    for event_item in tum_events:
        event_str += event_item.summary
        cal_event = event_item.gen_event()
        ncal.add_component(cal_event)

    return ncal.to_ical()