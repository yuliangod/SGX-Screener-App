# StonksApp spinoff from Stonks and Stonks2 repisotory, cleaned up and documented to the best of my ability with scalability in mind

Description: Investment analysis app to narrow down on companies to further analyse based on plots and numbers of relevant statistics

Features: 
1) Next and back buttons to look through companies ordered by estimated fair value
2) Like button to add interesting companies to a watchlist
3) Watchlist: View interested companies, can either remove or view page of the company 
4) Search bar within watchlist to directly jump to a particular company

Functions: 
- plot_chart: plot relevant graphs
- generate_info_dict: generate a dictionary containing relevant information for investment analysis
- update_main_frame: display charts and information from plot_chart and generate_info_dict on the app
- update_buttons_frame: arranges layout of buttons
! Update above functions to change visualisation of app, only need to update relevant function

- next, like, watchlist, settings(WIP): for functionality of buttons

Inputs:
fcff_df, sgx_df: dataframe containing relevant information to be displayed within app
! Future plans: input in a general df and choose which stats to show within app
