import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk

# Function to scrape Elon Musk's net worth from Forbes
def scrape_net_worth():
    url = 'https://www.forbes.com/profile/elon-musk/?sh=26393f27999b'
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/91.0.4472.124 Safari/537.36'
        )
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
    except requests.RequestException as e:
        messagebox.showerror("Network Error", f"Failed to retrieve data: {e}")
        return "$0B"  # Default value in case of error
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the net worth value
    net_worth_div = soup.find('div', class_='profile-info__item-value')
    if not net_worth_div:
        messagebox.showerror("Parsing Error", "Could not find net worth information on the page.")
        return "$0B"  # Default value in case of parsing error
    
    net_worth_str = net_worth_div.text.strip()
    
    return net_worth_str

# Function to convert USD net worth to AUD
def convert_usd_to_aud(net_worth_str, exchange_rate=1.6):
    """
    Converts a net worth string from USD to AUD.
    Example: '$200B' -> '320B AUD'
    """
    try:
        # Remove '$' and 'B' and convert to float
        net_worth_usd = float(net_worth_str.replace('$', '').replace('B', ''))
        net_worth_aud = net_worth_usd * 1e9 * exchange_rate  # Convert to AUD
        net_worth_aud_billion = net_worth_aud / 1e9  # Convert back to billions for display
        net_worth_aud_str = f"{net_worth_aud_billion:.2f}B"
        return net_worth_aud_str, net_worth_aud
    except ValueError:
        messagebox.showerror("Conversion Error", "Failed to convert net worth to AUD.")
        return "0B AUD", 0.0

# Function to calculate earnings per second needed to match Elon Musk's net worth in one year
def calculate_earnings_per_second(net_worth_aud):
    """
    Calculates the amount of AUD you need to earn per second to reach the net worth in one year.
    """
    seconds_in_a_year = 365 * 24 * 60 * 60
    earnings_per_second = net_worth_aud / seconds_in_a_year
    return earnings_per_second

# Function to calculate the time needed to match Elon Musk's net worth given annual earnings
def calculate_time_to_match_net_worth(net_worth_aud, annual_earnings):
    """
    Calculates the number of years needed to reach the net worth based on annual earnings.
    """
    if annual_earnings == 0:
        return float('inf')  # Avoid division by zero
    years_needed = net_worth_aud / annual_earnings
    return years_needed

# Function to update the net worth display and calculations
def update_net_worth():
    net_worth_usd_str = scrape_net_worth()
    net_worth_aud_str, net_worth_aud = convert_usd_to_aud(net_worth_usd_str)
    
    net_worth_label.config(text=f"Elon Musk's net worth is ${net_worth_aud_str} AUD today.")
    
    earnings_per_second = calculate_earnings_per_second(net_worth_aud)
    result_label.config(
        text=(
            f"To be worth ${net_worth_aud_str} in one year, "
            f"you need to earn ${earnings_per_second:.2f} per second."
        )
    )
    
    annual_earnings_input = earnings_entry.get().strip()
    if annual_earnings_input:
        try:
            annual_earnings = float(annual_earnings_input)
            if annual_earnings <= 0:
                messagebox.showerror("Input Error", "Annual earnings must be a positive number.")
                time_result_label.config(text="")
                return
            years_needed = calculate_time_to_match_net_worth(net_worth_aud, annual_earnings)
            if years_needed == float('inf'):
                time_result_label.config(text="Annual earnings cannot be zero.")
            else:
                time_result_label.config(
                    text=(
                        f"To be worth ${net_worth_aud_str}, "
                        f"you will need to earn ${annual_earnings:.2f} "
                        f"every year for {years_needed:.2f} years!"
                    )
                )
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric value for annual earnings.")
            time_result_label.config(text="")
    else:
        time_result_label.config(text="")

# Create the GUI using ThemedTk
root = ThemedTk(theme="breeze")  # Initialize with ttkthemes and set a desired theme
root.title("Elon Musk Net Worth Tracker")
root.geometry("900x250")  # Set a default window size

# Configure window resizing behavior
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Main content frame
content_frame = ttk.Frame(root, padding=(20, 10))
content_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Net Worth Label
net_worth_label = ttk.Label(
    content_frame, 
    text="Elon Musk's net worth is AUD 0.00B today.",
    font=("Helvetica", 14)
)
net_worth_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

# Annual Earnings Input
earnings_label = ttk.Label(
    content_frame, 
    text="Enter your annual earnings in AUD (optional):",
    font=("Helvetica", 12)
)
earnings_label.grid(row=1, column=0, columnspan=2, pady=(0, 5), sticky="w")

earnings_entry = ttk.Entry(content_frame)
earnings_entry.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky="ew")

# Result Labels
result_label = ttk.Label(content_frame, text="", font=("Helvetica", 12))
result_label.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky="w")

time_result_label = ttk.Label(content_frame, text="", font=("Helvetica", 12))
time_result_label.grid(row=4, column=0, columnspan=2, pady=(0, 10), sticky="w")

# Refresh Button
refresh_button = ttk.Button(
    content_frame, 
    text="Calculate (also updates net worth)", 
    command=update_net_worth
)
refresh_button.grid(row=5, column=0, columnspan=2, pady=(0, 10))

# Make the entry field expand horizontally
content_frame.columnconfigure(0, weight=1)
content_frame.columnconfigure(1, weight=1)
earnings_entry.focus_set()

# Initial update
update_net_worth()

# Run the GUI main loop
root.mainloop()

