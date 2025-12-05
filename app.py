import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. Generate Mock Trading Data (as MT5 is not installable) ---
# This section replaces direct MT5 connection.
np.random.seed(42) # for reproducibility

num_trades = 50 # Increased number of trades for more data
symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDCAD', 'XAUUSD']
trade_types = ['buy', 'sell']

data = {
    'time': [datetime.now() - timedelta(days=np.random.randint(1, 90), minutes=np.random.randint(1, 1440)) for _ in range(num_trades)],
    'symbol': np.random.choice(symbols, num_trades),
    'type': np.random.choice(trade_types, num_trades),
    'volume': np.round(np.random.uniform(0.01, 2.0, num_trades), 2),
    'price_open': np.round(np.random.uniform(1.0, 1.5, num_trades), 5),
    'price_close': np.round(np.random.uniform(1.0, 1.5, num_trades), 5),
    'profit': np.round(np.random.uniform(-1000.0, 2500.0, num_trades), 2)
}

df_trades = pd.DataFrame(data)

# Ensure price_close reflects profit/loss for 'buy'/'sell' logically
# Adjusting this logic slightly for more realistic price movements proportional to profit/volume
for i, row in df_trades.iterrows():
    if row['type'] == 'buy':
        if row['profit'] > 0:
            # Price increases for profit in buy
            df_trades.loc[i, 'price_close'] = row['price_open'] + abs(row['profit']) / (row['volume'] * 100000) 
        else:
            # Price decreases for loss in buy
            df_trades.loc[i, 'price_close'] = row['price_open'] - abs(row['profit']) / (row['volume'] * 100000)
    elif row['type'] == 'sell':
        if row['profit'] > 0:
            # Price decreases for profit in sell
            df_trades.loc[i, 'price_close'] = row['price_open'] - abs(row['profit']) / (row['volume'] * 100000)
        else:
            # Price increases for loss in sell
            df_trades.loc[i, 'price_close'] = row['price_open'] + abs(row['profit']) / (row['volume'] * 100000)

df_trades['price_close'] = np.round(df_trades['price_close'], 5)

# Sort by time
df_trades = df_trades.sort_values(by='time').reset_index(drop=True)

# --- 2. Calculate Key Trading Metrics ---

# Calculate the total PNL
total_pnl = df_trades['profit'].sum()

# Calculate the total number of trades
total_trades = len(df_trades)

# Determine the number of winning trades
winning_trades_count = df_trades[df_trades['profit'] > 0].shape[0]

# Calculate the win rate
win_rate = (winning_trades_count / total_trades) * 100 if total_trades > 0 else 0

# Calculate the average profit for winning trades
winning_trades = df_trades[df_trades['profit'] > 0]
average_gain = winning_trades['profit'].mean() if not winning_trades.empty else 0

# Calculate the average loss for losing trades
losing_trades = df_trades[df_trades['profit'] < 0]
average_loss = losing_trades['profit'].mean() if not losing_trades.empty else 0 # Average loss will be negative

# Prepare the data for the equity curve
df_trades['equity_curve'] = df_trades['profit'].cumsum()

# Calculate the maximum drawdown
df_trades['peak'] = df_trades['equity_curve'].cummax()
df_trades['drawdown'] = df_trades['peak'] - df_trades['equity_curve']
max_drawdown = df_trades['drawdown'].max()

# --- Streamlit Dashboard Layout ---
st.set_page_config(page_title='Disciplined Trade Dashboard', layout='wide')

# Sidebar for Customization
st.sidebar.subheader('Dashboard Customization')
primary_color = st.sidebar.color_picker('Select Primary Color', '#1E90FF')
profit_color = st.sidebar.color_picker('Select Profit Color', '#3CB371')
loss_color = st.sidebar.color_picker('Select Loss Color', '#DC143C')
st.sidebar.markdown('---')
st.sidebar.write('Customize your dashboard colors.')

# Apply custom CSS for colors (basic example, can be expanded)
st.markdown(f"""
    <style>
    .st-emotion-cache-1wv9v3u {{ color: {primary_color}; }}
    .st-emotion-cache-nahz7x {{ color: {primary_color}; }}
    </style>
    """, unsafe_allow_html=True)

# Main Title and Branding
st.title('Disciplined Trade Analysis')
st.markdown("### Your comprehensive trading performance overview")

# --- Display Key Statistics ---
st.subheader('Trading Performance Overview')
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label="Total PNL", value=f"{total_pnl:,.2f}", delta_color="off",
              help="Total Profit and Loss across all trades.")

with col2:
    st.metric(label="Win Rate", value=f"{win_rate:.2f}%", delta_color="off",
              help="Percentage of winning trades.")

with col3:
    st.metric(label="Total Trades", value=f"{total_trades}", delta_color="off",
              help="Total number of trades executed.")

with col4:
    st.metric(label="Avg. Winning Trade", value=f"{average_gain:,.2f}", delta_color="off",
              help="Average profit for winning trades.")

with col5:
    st.metric(label="Avg. Losing Trade", value=f"{average_loss:,.2f}", delta_color="off",
              help="Average loss for losing trades.")

st.metric(label="Maximum Drawdown", value=f"{-max_drawdown:,.2f}", delta_color="inverse",
          help="The largest peak-to-trough decline in the equity curve.")

# --- Performance Visualizations ---
st.subheader('Performance Visualizations')

# 1. PNL Bar Chart
df_trades['pnl_color'] = df_trades['profit'].apply(lambda x: 'Profit' if x > 0 else 'Loss')
fig_pnl = px.bar(
    df_trades.reset_index(),
    x='index',
    y='profit',
    color='pnl_color',
    color_discrete_map={'Profit': profit_color, 'Loss': loss_color},
    title='PNL per Trade',
    labels={'index': 'Trade Number', 'profit': 'Profit/Loss'}
)
fig_pnl.update_layout(showlegend=False)
st.plotly_chart(fig_pnl, width='stretch') 

# 2. Equity Curve Line Chart
fig_equity = px.line(
    df_trades,
    x='time',
    y='equity_curve',
    title='Cumulative Equity Curve',
    labels={'time': 'Date', 'equity_curve': 'Equity'}
)
fig_equity.update_traces(line_color=primary_color)
st.plotly_chart(fig_equity, width='stretch') 

# --- Interactive Daily Trade Calendar ---
st.subheader('Interactive Daily Trade Calendar')

df_trades['time'] = pd.to_datetime(df_trades['time'])
daily_pnl_data = df_trades.groupby(df_trades['time'].dt.date)['profit'].sum().reset_index()
daily_pnl_data.columns = ['Date', 'Daily PNL']
daily_pnl_data['Date'] = pd.to_datetime(daily_pnl_data['Date'])

min_date = daily_pnl_data['Date'].min()
max_date = daily_pnl_data['Date'].max()
full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')

calendar_data = pd.DataFrame(full_date_range, columns=['Date'])
calendar_data = pd.merge(calendar_data, daily_pnl_data, on='Date', how='left').fillna(0)

calendar_data['Year'] = calendar_data['Date'].dt.year
calendar_data['Month'] = calendar_data['Date'].dt.month
calendar_data['Day'] = calendar_data['Date'].dt.day
calendar_data['DayOfWeek'] = calendar_data['Date'].dt.dayofweek # Monday=0, Sunday=6
calendar_data['Week'] = calendar_data['Date'].dt.isocalendar().week.astype(int)

fig_calendar = go.Figure(data=go.Heatmap(
    x=calendar_data['DayOfWeek'],
    y=calendar_data['Week'],
    z=calendar_data['Daily PNL'],
    colorscale=[[0, loss_color], [0.5, 'white'], [1, profit_color]], # Custom colorscale
    colorbar_title='Daily PNL',
    text=calendar_data.apply(lambda row: f"{row['Day']}<br>PNL: {row['Daily PNL']:.2f}", axis=1),
    hoverinfo='text'
))

fig_calendar.update_layout(
    title='Daily PNL Calendar',
    xaxis=dict(
        tickmode='array',
        tickvals=[0, 1, 2, 3, 4, 5, 6],
        ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ),
    yaxis_nticks=calendar_data['Week'].nunique(),
    yaxis_autorange='reversed',
    height=600
)

st.plotly_chart(fig_calendar, width='stretch') 

# --- Display All Trades Table ---
st.subheader('All Trades Data')
st.dataframe(df_trades, width='stretch') 

# --- Export Data Functionality ---
st.subheader('Export Data')
csv_data = df_trades.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Trade Data as CSV",
    data=csv_data,
    file_name='disciplined_trades.csv',
    mime='text/csv',
    help="Click here to download your trading data in CSV format."
)
