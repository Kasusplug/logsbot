
class Logs:

    def __init__(self, file_name_read, file_name_record):
        self.file_name_read = file_name_read
        self.file_name_record = file_name_record
        self.logs_time_count_info = {}
        self.logs_time_count_error = {}
        self.logs_time_count_debug = {}


    def logs_find(self):
        with open(self.file_name_read, 'r', encoding='utf8') as logs_events:
            with open(self.file_name_record, 'w', encoding='utf8') as new_logs:        
                for line in logs_events:
                    if line.strip().find("[INFO]"):
                        timestamp = line[1:47]  
                        if timestamp in self.logs_time_count_info:
                            self.logs_time_count_info[timestamp] += 1  
                        else:
                            self.logs_time_count_info[timestamp] = 1  
                        new_logs.write(line[1:47] + '\n')
                    if line.strip().find("[ERROR]"):
                        timestamp = line[1:47]
                        if timestamp in self.logs_time_count_error:
                            self.logs_time_count_error[timestamp] += 1  
                        else:
                            self.logs_time_count_error[timestamp] = 1  
                        new_logs.write(line[1:47] + '\n')
                    if line.strip().find("[DEBUG]"):
                        timestamp = line[1:47]
                        if timestamp in self.logs_time_count_debug:
                            self.logs_time_count_debug[timestamp] += 1  
                        else:
                            self.logs_time_count_debug[timestamp] = 1  
                        new_logs.write(line[1:47] + '\n')
                print('Succesfully get all logs')


check_logs = Logs(file_name_read=r'task_1try\logs.log',
                   file_name_record=r'task_1try\cathed_logs.log')
check_logs.logs_find()