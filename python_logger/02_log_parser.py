
class Logs:

    def __init__(self, file_name_read, file_name_record):
        self.file_name_read = file_name_read
        self.file_name_record = file_name_record
        self.hours_count = {}
        self.months_count = {}
        self.years_count = {}
        self.logs_time_count = {}

    def nok_logs(self):
        with open(self.file_name_read, 'r', encoding='utf8') as logs_events:
            with open(self.file_name_record, 'w', encoding='utf8') as new_logs:        
                for line in logs_events:
                    if line.strip().endswith('NOK'):
                        timestamp = line[1:17]  
                        if timestamp in self.logs_time_count:
                            self.logs_time_count[timestamp] += 1  
                        else:
                            self.logs_time_count[timestamp] = 1  
                        new_logs.write(line[1:17] + '\n')
                print('Succesfully get NOK logs')

    def nok_logs_counter(self):
        with open('python_logger\logs.txt', 'w', encoding='utf8') as new_logs:
            for timestamp, count in self.logs_time_count.items():
                new_logs.write(f"[{timestamp}] {count}" + '\n')
            print('Succesfully counted logs')

    def hours_stats(self):
        for timestamp, count in self.logs_time_count.items():
            hour = timestamp[11:13]
            if hour in self.hours_count:
                self.hours_count[hour] += count
            else:
                self.hours_count[hour] = count
        return [print(f"Hour: {hour}, Quantity: {count}")
                 for hour, count in self.hours_count.items()]

    def months_stats(self):
        for timestamp, count in self.logs_time_count.items():
            month = timestamp[5:7]
            if month in self.months_count:
                self.months_count[month] += count
            else:
                self.months_count[month] = count
        return [print(f"Month: {month}, Quantity: {count}")
                 for hour, count in self.months_count.items()]

    def year_stats(self):
        for timestamp, count in self.logs_time_count.items():
            year = timestamp[:4]
            if year in self.years_count:
                self.years_count[year] += count
            else:
                self.years_count[year] = count
        return [print(f"Year: {year}, Quantity: {count}")
                 for hour, count in self.years_count.items()]

check_logs = Logs(file_name_read='python_logger\events.txt',
                   file_name_record='python_logger\logs.txt')
check_logs.nok_logs()
check_logs.nok_logs_counter()
check_logs.hours_stats()
check_logs.months_stats()
check_logs.year_stats()
 

#         with open('dz-9\\events.txt', 'r', encoding='utf8') as logs_events:
#             with open('.\\dz-9\\logs.txt', 'w', encoding='utf8') as new_logs:        
#                 for line in logs_events:
#                     if line.strip().endswith('NOK'):
#                         timestamp = line[1:17]  
#                         if timestamp in logs_time_count:
#                             logs_time_count[timestamp] += 1  
#                         else:
#                             logs_time_count[timestamp] = 1  
#                         new_logs.write(line[1:17] + '\n')

# with open('.\\dz-9\\logs.txt', 'w', encoding='utf8') as new_logs:
#     for timestamp, count in logs_time_count.items():
#         new_logs.write(f"[{timestamp}] {count}" + '\n')

# hours_count = {}
# months_count = {}
# years_count = {}

# for timestamp, count in logs_time_count.items():
#     hour = timestamp[11:13]
#     if hour in hours_count:
#         hours_count[hour] += count
#     else:
#         hours_count[hour] = count

#     month = timestamp[5:7]
#     if month in months_count:
#         months_count[month] += count
#     else:
#         months_count[month] = count

#     year = timestamp[:4]
#     if year in years_count:
#         years_count[year] += count
#     else:
#         years_count[year] = count

# print("Sorted by Hours:")
# for hour, count in hours_count.items():
#     print(f"Час: {hour}, Quantity: {count}")

# print("\nSorted by Month:")
# for month, count in months_count.items():
#     print(f"Month: {month}, Quantity: {count}")

# print("\nSorted by Years:")
# for year, count in years_count.items():
#     print(f"Year: {year}, Quantity: {count}")