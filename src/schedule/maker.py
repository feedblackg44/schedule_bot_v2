import logging
from datetime import time

import yaml

from enums import Weekday
from schedule import Teacher, Discipline, Schedule
from schedule.calendar import Day, Lesson, Week


class Maker:
    def __init__(self, path):
        self.logger = logging.getLogger(__name__)
        self.path = path

    def make(self):
        self.logger.info(f"Загрузка расписания из файла {self.path}")
        with open(self.path, "r", encoding='UTF-8') as file:
            schedule_file = yaml.safe_load(file)

        if schedule_file is None:
            self.logger.error(f"Файл {self.path} пуст")
            return

        timetable = [{'start': time.fromisoformat(time_['start']),
                      'end': time.fromisoformat(time_['end'])}
                     for time_ in schedule_file['timetable']]
        teachers = {teacher['name']: Teacher(**teacher)
                    for teacher in schedule_file['teachers']}
        disciplines = {}
        for discipline in schedule_file['disciplines']:
            if isinstance(discipline['lecture'], str):
                discipline['lecture'] = [teachers[discipline['lecture']]]
            else:
                discipline['lecture'] = [teachers[teacher] for teacher in discipline['lecture']]
            if 'practice' in discipline:
                if isinstance(discipline['practice'], str):
                    discipline['practice'] = [teachers[discipline['practice']]]
                else:
                    discipline['practice'] = [teachers[teacher] for teacher in discipline['practice']]
            disciplines[discipline['name']] = Discipline(**discipline)
        schedule = schedule_file['schedule']

        days_keys = {
            'monday': Weekday.MONDAY,
            'tuesday': Weekday.TUESDAY,
            'wednesday': Weekday.WEDNESDAY,
            'thursday': Weekday.THURSDAY,
            'friday': Weekday.FRIDAY,
            'saturday': Weekday.SATURDAY,
            'sunday': Weekday.SUNDAY
        }
        days_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]

        weeks = []
        for w_idx, week in enumerate(schedule.values(), start=1):
            week_dict = {}
            for idx, (day, day_schedule) in enumerate(week.items()):
                day_dict = {}
                for lesson, disc_list in day_schedule.items():
                    di_list = []
                    for disc in disc_list:
                        di_list.append({
                            'discipline': disciplines[disc['name']],
                            'is_lecture': disc['is_lecture']
                        })
                    day_dict[lesson] = Lesson(di_list, timetable[lesson - 1])
                week_dict[days_keys[day]] = Day(days_keys[day], days_list[idx], day_dict)
            weeks.append(Week(w_idx, week_dict))

        return (Schedule(weeks, schedule_file['schedule_link'], timetable, schedule_file['group'],
                         schedule_file['extra']),
                teachers,
                disciplines)
