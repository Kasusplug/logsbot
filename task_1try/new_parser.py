from whole_outputs import info_output, error_output, debug_output


class Logs:

    def __init__(self, file_name_read, file_name_record):
        self.file_name_read = file_name_read
        self.file_name_record = file_name_record
        self.logs_time_count_info = {}
        self.logs_time_count_error = {}
        self.logs_time_count_debug = {}
        self.count_info = 0
        self.count_error = 0
        self.count_debug = 0

    def logs_find(self):
        with open(self.file_name_read, 'r', encoding='utf8') as logs_events:
            with open(self.file_name_record, 'w', encoding='utf8') as new_logs:        
                for line in logs_events:
                    line = line.strip()
                    if "[INFO]" in line:
                        timestamp = line[0:90] 
                        if timestamp in self.logs_time_count_info:
                            self.logs_time_count_info[timestamp] += 1  
                        else:
                            self.logs_time_count_info[timestamp] = 1  
                        new_logs.write(line + '\n')
                    elif "[ERROR]" in line:
                        timestamp = line[0:90]
                        if timestamp in self.logs_time_count_error:
                            self.logs_time_count_error[timestamp] += 1  
                        else:
                            self.logs_time_count_error[timestamp] = 1  
                        new_logs.write(line + '\n')
                    elif "[DEBUG]" in line:
                        timestamp = line[0:90]
                        if timestamp in self.logs_time_count_debug:
                            self.logs_time_count_debug[timestamp] += 1  
                        else:
                            self.logs_time_count_debug[timestamp] = 1  
                        new_logs.write(line + '\n')
                print('Successfully processed all logs')
    
    def logs_counter(self):
        with open(r'task_1try\cathed_logs.log', 'w', encoding='utf8') as new_logs:
            for timestamp, count in self.logs_time_count_info.items():
                new_logs.write(f"  {timestamp} - {count}" + '\n')
            for timestamp, count in self.logs_time_count_error.items():
                new_logs.write(f"  {timestamp} - {count}" + '\n')
            for timestamp, count in self.logs_time_count_debug.items():
                new_logs.write(f"  {timestamp} - {count}" + '\n')
            print('Succesfully counted ALL logs')


    def logs_compile(self):
        with open(r'task_1try\cathed_logs.log', 'r', encoding='utf8') as read_logs:
            with open(r'task_1try\counted.log', 'w', encoding='utf8') as counted_logs:
                for line in read_logs:
                    line = line.strip()

                    if any(info in line for info in info_output):
                        self.count_info += 1
                    elif any(error in line for error in error_output):
                        self.count_error += 1
                    elif any(debug in line for debug in debug_output):
                        self.count_debug += 1

                counted_logs.write(f"[INFO] logs count: {self.count_info}\n")
                counted_logs.write(f"[ERROR] logs count: {self.count_debug}\n")
                counted_logs.write(f"[DEBUG] logs count: {self.count_error}\n")

        print("Log counts successfully written to file")

check_logs = Logs(file_name_read=r'task_1try\logs.log',
                   file_name_record=r'task_1try\cathed_logs.log')
check_logs.logs_find()
check_logs.logs_counter()
check_logs.logs_compile()

