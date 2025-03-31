import psutil
import time
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

class SystemMonitor:
    def __init__(self, cpu_threshold=80, memory_threshold=80, disk_threshold=80):
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.disk_threshold = disk_threshold

    def check_cpu_usage(self):
        """Returns current CPU usage and threshold status"""
        usage = psutil.cpu_percent(interval=1)
        return usage, usage > self.cpu_threshold

    def check_memory_usage(self):
        """Returns current memory usage and threshold status"""
        mem = psutil.virtual_memory()
        return mem.percent, mem.percent > self.memory_threshold

    def check_disk_usage(self):
        """Returns current disk usage and threshold status"""
        disk = psutil.disk_usage('/')
        return disk.percent, disk.percent > self.disk_threshold

    def monitor_resources(self):
        """Check all resources and print status with colors"""
        cpu_usage, cpu_over = self.check_cpu_usage()
        mem_usage, mem_over = self.check_memory_usage()
        disk_usage, disk_over = self.check_disk_usage()

        # Print resource usage with colors
        print(Fore.CYAN + f"CPU Usage: {cpu_usage}%")
        print(Fore.GREEN + f"Memory Usage: {mem_usage}%")
        print(Fore.MAGENTA + f"Disk Usage: {disk_usage}%")

        # Print warnings in red if thresholds are exceeded
        if cpu_over:
            print(Fore.RED + f"Warning: CPU usage exceeds {self.cpu_threshold}% threshold!")
        if mem_over:
            print(Fore.RED + f"Warning: Memory usage exceeds {self.memory_threshold}% threshold!")
        if disk_over:
            print(Fore.RED + f"Warning: Disk usage exceeds {self.disk_threshold}% threshold!")
        print(Style.RESET_ALL + "-----------------------------------")

def print_main_menu():
    """Display the main menu with colored options"""
    print(Fore.BLUE + "\n--- System Monitoring Tool ---")
    print(Fore.YELLOW + "1. Run System Check")
    print(Fore.YELLOW + "2. Adjust Threshold Settings")
    print(Fore.YELLOW + "3. Exit")
    print(Fore.BLUE + "------------------------------" + Style.RESET_ALL)

def print_threshold_menu():
    """Display the threshold adjustment submenu"""
    print(Fore.BLUE + "\n--- Adjust Thresholds ---")
    print(Fore.YELLOW + "1. Change CPU Threshold")
    print(Fore.YELLOW + "2. Change Memory Threshold")
    print(Fore.YELLOW + "3. Change Disk Threshold")
    print(Fore.YELLOW + "4. Return to Main Menu")
    print(Fore.BLUE + "------------------------" + Style.RESET_ALL)

def get_valid_input(prompt, min_val=0, max_val=100):
    """Get and validate numerical input from user"""
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(Fore.RED + f"Error: Value must be between {min_val} and {max_val}!")
        except ValueError:
            print(Fore.RED + "Error: Please enter a valid number!")

def monitoring():
    monitor = SystemMonitor()
    
    while True:
        print_main_menu()
        choice = input(Fore.WHITE + "Enter your choice (1-3): ")

        if choice == '1':
            print(Fore.BLUE + "\nRunning System Check..." + Style.RESET_ALL)
            monitor.monitor_resources()
        
        elif choice == '2':
            while True:
                print_threshold_menu()
                sub_choice = input(Fore.WHITE + "Enter threshold option (1-4): ")
                
                if sub_choice == '1':
                    new_threshold = get_valid_input("Enter new CPU threshold (%): ")
                    monitor.cpu_threshold = new_threshold
                    print(Fore.GREEN + f"CPU threshold updated to {new_threshold}%")
                
                elif sub_choice == '2':
                    new_threshold = get_valid_input("Enter new Memory threshold (%): ")
                    monitor.memory_threshold = new_threshold
                    print(Fore.GREEN + f"Memory threshold updated to {new_threshold}%")
                
                elif sub_choice == '3':
                    new_threshold = get_valid_input("Enter new Disk threshold (%): ")
                    monitor.disk_threshold = new_threshold
                    print(Fore.GREEN + f"Disk threshold updated to {new_threshold}%")
                
                elif sub_choice == '4':
                    break
                
                else:
                    print(Fore.RED + "Invalid option! Please try again.")
        
        elif choice == '3':
            print(Fore.BLUE + "\nExiting system monitor. Goodbye!" + Style.RESET_ALL)
            break
        
        else:
            print(Fore.RED + "Invalid choice! Please enter a number between 1-3.")

if __name__ == "__main__":
    monitoring()