from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fcff_df = pd.read_excel('FCFF_analysis_filtered.xlsx', index_col=[0])
sgx_df = pd.read_csv('myData.csv', index_col=[1])

class StonksApp:
    def __init__(self, master):
        self.master = master
        master.title("StonkApp")

        # Initialise app variables
        self.idx = 0
        self.current_stock = fcff_df.index[self.idx]

        # Set up frame with charts and stats
        self.update_main_frame(self.generate_info_dict())

        # Set up frame for app buttons
        self.update_buttons_frame()

    def plot_chart(self, row: int, column: int, *args: pd.DataFrame, columnspan: int=2, title: str="", xlabel: str="", ylabel: str=""):
        """ Function to plot graphs on same chart from dataframes passed into the function as arguments
        
        :param row, column, and columnspan: variables for Tkinter grid styling
        :param title, xlablel, ylabel: variables for matplotlib chart 
        :param *args: dataframes to be plotted onto chart
        """

        # Setting up of chart
        figure = plt.Figure(figsize=(6,5), dpi=70)
        ax = figure.add_subplot(111)
        line_graph = FigureCanvasTkAgg(figure, self.main_frame)
        line_graph.get_tk_widget().grid(row=row, column=column, columnspan=columnspan)

        # Plotting graphs
        for df in args:
            df.plot(kind='line', legend=True, ax=ax)

        # Chart styling
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

    def generate_info_dict(self) -> dict:
        """ Function to generate a dictionary of info name and info value pairs to be displayed in app 
        
        :return: info_dict
        """

        info_dict = {}

        # Show name of stock
        trading_code = self.current_stock.replace(".SI", "")
        self.trading_name = sgx_df.loc[trading_code, "Trading Name"]
        info_dict["Name"] = self.trading_name 

        # Show sector of stock
        self.sector = sgx_df.loc[trading_code, "Sector"]    
        info_dict["Sector"] = self.sector

        # Show wacc of stock
        self.wacc = fcff_df.loc[self.current_stock, "WACC"]      
        info_dict["WACC"] = self.wacc

        # Show fcf of stock
        self.fcff = fcff_df.loc[self.current_stock, "FCFF"]
        self.shares_out = fcff_df.loc[self.current_stock, "Shares outstanding"]
        self.fcf = self.fcff/self.shares_out
        info_dict["FCF"] = self.fcf

        # Show fair value stat
        self.fair_value = fcff_df.loc[self.current_stock, "Fair value"]   
        info_dict["Fair value"] = self.fair_value

        # Show percentage undervalued stat
        self.percentage_undervalued = fcff_df.loc[self.current_stock, "Percentage undervalued"]   
        info_dict["Percentage undervalued"] = self.percentage_undervalued

        return info_dict

    def update_main_frame(self, info_dict: dict):
        """ Function to populate main frame """

        self.main_frame = Frame(self.master)
        self.main_frame.grid(row=0, column=0)

        # Update variables
        self.IS_df = pd.read_csv(f"Database/{self.current_stock}/IS.csv", index_col=[0])
        self.BS_df = pd.read_csv(f"Database/{self.current_stock}/BS.csv", index_col=[0])
        self.CF_df = pd.read_csv(f"Database/{self.current_stock}/CF.csv", index_col=[0])

        # Graphs to be plotted
        self.revenue_df = self.IS_df.loc["Revenue"]
        self.revenue_df = self.revenue_df.astype(float)

        self.operating_income_df = self.IS_df.loc["Operating Income"] 
        self.operating_income_df=self.operating_income_df.astype(float)

        # Plot graph of revenue and operating income
        self.plot_chart(0, 0, self.revenue_df, self.operating_income_df, title="", xlabel="Year", ylabel="")

        # Display useful information
        for i, key in enumerate(info_dict):
            Label(self.main_frame, text= f"{key}: \n{info_dict[key]}", font='Helvetica 10').grid(row=(i//2)+1, column=i%2)

    def update_buttons_frame(self):
        """ Function to populate button frame with back, next, like, and watchlist buttons """
        """ Arranges layout of buttons """
        self.button_frame = Frame(self.master)

        # Back button
        self.back_button = Button(self.button_frame, text="Back", command=lambda: self.next(self.idx - 1))
        self.back_button.grid(row=0, column=0, pady="10", padx="10")

        # Next button
        self.next_button = Button(self.button_frame, text="Next", command=lambda: self.next(self.idx + 1))
        self.next_button.grid(row=0, column=1)

        # Like button
        self.like_button = Button(self.button_frame, text="Like", command=self.like)
        self.like_button.grid(row=1, column=0, pady="5", padx="10")

        # Toggle like button if stock is in watchlist
        self.toggle_like_button()

        # Watchlist button
        self.watchlist_button = Button(self.button_frame, text="Watchlist", command=self.watchlist)
        self.watchlist_button.grid(row=1, column=1, pady="5", padx="10")

        # Frame palcement
        self.button_frame.grid(row=1, column=0)

    def toggle_like_button(self):
        """ Toggle like button based on whether self.current_stock is in watchlist """

        with open("Cache/watchlist.txt", "r") as watchlist:
            lines = watchlist.readlines()
        if str(self.current_stock + '\n') in lines:
            self.like_button.config(relief="sunken")
        else:
            self.like_button.config(relief="raised")

    
    """ Functions to make buttons interactable """

    def next(self, idx):
        """ Function for next button to show next or previous stock """
        # Update variables
        self.idx = idx
        self.current_stock = fcff_df.index[self.idx]

        self.update_main_frame(self.generate_info_dict())

        # Toggle like button based on whether stock is in watchlist
        self.toggle_like_button()

    def like(self):     
        """ Function for like button to add stock to watchlist """

        if self.like_button.config('relief')[-1] == 'sunken':
            self.like_button.config(relief="raised")
            with open("Cache/watchlist.txt", "r") as f:
                lines = f.readlines()
            with open("Cache/watchlist.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != self.current_stock:
                        f.write(line)
        else:
            with open("Cache/watchlist.txt", "a") as myfile:
                myfile.write(f"{self.current_stock}\n")
            self.like_button.config(relief="sunken")

    def watchlist(self):
        """ Function to see stocks in watchlist """

        def view_watchlist_stock(stock):
            """ Function for view button to look at selected stock """
            watchlist_window.destroy()
            self.master.deiconify()
            self.update_main_frame(self.generate_info_dict())
            self.current_stock = stock
            self.update_buttons_frame()

            #update self.idx to that of stock
            self.idx = list(fcff_df.index).index(stock)

        def delete_watchlist_stock(stock):
            """ Function for delete button to delete selected stock """

            with open("Cache/watchlist.txt", "r") as f:
                lines = f.readlines()
            with open("Cache/watchlist.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != stock:
                        f.write(line)
            
            idx = Lines.index(stock+'\n')
            labels[idx].destroy()
            view_buttons[idx].destroy()
            delete_buttons[idx].destroy()

            if len(lines) == 1:
                Label(second_frame, text='Watchlist is currently empty', font='Helvetica 10').grid(column=0)

            #untoggle like button on main window if stock on that window is removed from watchlist
            if stock == self.current_stock:
                self.update_buttons_frame()
        
        def search():
            """ Function for search button to search for a specified stock by its full ticker """
            search_ticker = search_entry.get()
            if search_ticker in fcff_df.index:
                view_watchlist_stock(search_ticker)
        
            else:
                messagebox.showerror("Error","Sorry the ticker you entered was not found within this spreadsheet")
                return

        def on_closing():
            """ Function to make main window reappear on closing of watchlist window """
            watchlist_window.destroy()
            self.master.deiconify()

        def back_to_main_button_command():
            """ Function to get back to main app when button is clicked"""
            watchlist_window.destroy()
            self.master.deiconify()

        # Create new window over current window
        self.master.withdraw()  # hide main window
        watchlist_window = Toplevel(self.master)
        watchlist_window.protocol("WM_DELETE_WINDOW", on_closing)  # make main window reappear on closing
        watchlist_window.title("Watchlist")
        watchlist_window.geometry("400x500")

        # Create search bar
        search_frame = Frame(watchlist_window)
        search_frame.pack()
        search_entry = Entry(search_frame)
        search_entry.pack(side=LEFT)
        search_button = Button(search_frame, text='Search', command=search)
        search_button.pack(side=LEFT)

        # Create a button to get back to main app
        back_to_main_button = Button(watchlist_window, text="Back to main app", command=back_to_main_button_command)
        back_to_main_button.pack(pady=5)

        ##### scroll button #####
        # Create A Main Frame
        main_frame = Frame(watchlist_window)
        main_frame.pack(fill=BOTH, expand=1)

        # Create A Canvas
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbar To The Canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        def _on_mouse_wheel(event):
            my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

        my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        # Create ANOTHER Frame INSIDE the Canvas
        second_frame = Frame(my_canvas)

        # Add that New frame To a Window In The Canvas
        my_canvas.create_window((0,0), window=second_frame, anchor="nw")

        ##### end of scroll bar #####

        # Get list of stocks in watchlist
        file1 = open('Cache/watchlist.txt', 'r')
        Lines = file1.readlines()

        if len(Lines) == 0:
            Label(second_frame, text='Watchlist is currently empty', font='Helvetica 10').grid(column=0)

        labels = []     # Create empty lists to reference which ones to delete later on
        view_buttons = []
        delete_buttons = []

        # Display stocks in watchlist, with buttons to view or delete stock
        for i in range(len(Lines)):
            watchlist_stock_label = Label(second_frame, text=Lines[i], font='Helvetica 10')
            watchlist_stock_label.grid(row=i, column=0)
            watchlist_stock_button = Button(second_frame, text='View', command=lambda i=i: view_watchlist_stock(Lines[i].strip()))
            watchlist_stock_button.grid(row=i, column=1)
            delete_watchlist_stock_button = Button(second_frame, text='Remove', command=lambda i=i:delete_watchlist_stock(Lines[i].strip()))
            delete_watchlist_stock_button.grid(row=i, column=2)

            labels.append(watchlist_stock_label)
            view_buttons.append(watchlist_stock_button)
            delete_buttons.append(delete_watchlist_stock_button)

    def settings(self):
        pass

if __name__ == "__main__":
    root = Tk()
    StonksApp(root)
    root.mainloop()
