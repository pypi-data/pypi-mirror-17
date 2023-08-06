import collections
from django.core.management import BaseCommand

from ...exceptions import ACPCalendarException
from ...models import ACPHoliday, HolidayType
from ...initial_data import HOLIDAYS_INITIAL_DATA


class Command(BaseCommand):
    '''
    $ python manage.py acp_holidays --list-initial

    You will get a print out like this. The [*] on the first column means that the initial data
    is already on the database.  The [-] on the first column means that the initial data
    is not on the database.

    Year 2006  (11 holidays)
    ----------------------------------------------------------------------
	[*] año_nuevo                      2006-01-01
	[-] mártires                       2006-01-09
	[*] martes_carnaval                2006-02-28
	[*] viernes_santo                  2006-04-14
	[*] día_del_trabajo                2006-05-01

    ...

    ======================================================================
    Found 133 in initials
    Found 132 in database


    '''
    def add_arguments(self, parser):
        #parser.add_argument('optional-argument', nargs='?')
        parser.add_argument('--list-initial',
                            action='store_true',
                            dest='list_initial',
                            default=None,
                            help='List initial data')
        # parser.add_argument('--variable',
        #                     action='store',
        #                     dest='variable_name',
        #                     default=None,
        #                     help='Useful info')
        # parser.add_argument('--appended-argument',
        #                     action='append',
        #                     dest='appended_arg',
        #                     default=None,
        #                     help='Useful info')

    def handle(self, *args, **options):
        if options['list_initial']:
            count_initial_holidays = 0
            count_db_holidays = 0
            ordered_holidays = collections.OrderedDict(sorted(HOLIDAYS_INITIAL_DATA.items()))
            for year, holidays in ordered_holidays.items():
                self.stdout.write('Year %d  (%d holidays)' % (year, len(holidays)))
                self.stdout.write('-'*70)
                for holiday in holidays:
                    display = dict()
                    display['found'] = '*'
                    display['date'] = holiday['date'].strftime('%Y-%m-%d')
                    count_initial_holidays += 1
                    try:
                        if isinstance(holiday['holiday_type'], str):
                            short_name = holiday['holiday_type']
                        elif type(holiday['holiday_type']).__name__ == 'HolidayType':
                            short_name = holiday['holiday_type'].short_name
                        else:
                            msg = 'Holiday type must be either an instance of str or of HolidayType. ' \
                                  'Your are using an instance of %s' % holiday['holiday_type'].__class__.__name__
                            raise ACPCalendarException(msg)
                        display['holiday_type'] = short_name
                        ACPHoliday.objects.get(holiday_type__short_name=short_name,
                                                             date=holiday['date'])
                        count_db_holidays += 1
                    except ACPHoliday.DoesNotExist:
                       display['found'] = '-'
                    self.stdout.write('\t[{found}] {holiday_type:<30} {date}'.format(**display))
                self.stdout.write('='*70)
            self.stdout.write('Found %d in initials' % count_initial_holidays)
            self.stdout.write('Found %d in database' % count_db_holidays)
