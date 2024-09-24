
class Logs:

    def __init__(self, file_name_read, file_name_record):
        self.file_name_read = file_name_read
        self.file_name_record = file_name_record


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


check_logs = Logs(file_name_read='python_logger\events.txt',
                   file_name_record='python_logger\logs.txt')
check_logs.nok_logs()