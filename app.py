import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read the CSV data from the provided link
url = 'https://github.com/renjanay/plotly/raw/main/Data.xlsx'
df = pd.read_excel(url)

# Create the Dash app
app = dash.Dash(__name__)

# Line chart: Relation between bulan and pend_total
line_chart = px.line(df, x='bulan', y='pend_total', title='Line Chart: Pendapatan Total vs. Bulan')

# Find the high point and low point of the line chart according to pend_total
max_point = df[df['pend_total'] == df['pend_total'].max()]
min_point = df[df['pend_total'] == df['pend_total'].min()]

# Pie chart: Relation between diskon (excluding 0% and 100%) and sum of qty
df_filtered = df[(df['diskon'] > 0) & (df['diskon'] < 100)]
diskon_qty_pie_chart = px.pie(df_filtered, values='qty', names='diskon', title='Pie Chart: Sum of Qty by Diskon')

# Find the diskon with the largest sum of qty
largest_qty_diskon = df_filtered.groupby('diskon')['qty'].sum().idxmax()

# Pie chart: Relation between jenis_penjualan (excluding giveaway) and sum of qty
df_jenis_penjualan_filtered = df[df['jenis_penjualan'] != 'giveaway']
jenis_penjualan_qty_pie_chart = px.pie(df_jenis_penjualan_filtered, values='qty', names='jenis_penjualan',
                                      title='Pie Chart: Sum of Qty by Jenis Penjualan')

# Find the jenis_penjualan with the largest sum of qty
largest_qty_jenis_penjualan = df_jenis_penjualan_filtered.groupby('jenis_penjualan')['qty'].sum().idxmax()

# Dual combination chart: Relation between month of tgl_prod, count of barang_jual, and count of barang_prod
combination_chart = go.Figure()

combination_chart.add_trace(go.Bar(x=df['tgl_prod'], y=df['barang_jual'], name='Barang Jual'))
combination_chart.add_trace(go.Scatter(x=df['tgl_prod'], y=df['barang_prod'], mode='lines', yaxis='y2', name='Barang Prod'))

combination_chart.update_layout(title='Dual Combination Chart: Barang Jual and Barang Prod',
                                yaxis=dict(title='Barang Jual'),
                                yaxis2=dict(title='Barang Prod', overlaying='y', side='right'))

# Table: Relation between prov (excluding Singapura), kategori, jenis_barang and sum of qty
df_filtered_prov = df[df['prov'] != 'Singapura']
table_data = df_filtered_prov.groupby(['prov', 'kategori', 'jenis_barang'])['qty'].sum().reset_index()
table_data = table_data.sort_values(by='qty', ascending=False)

table = go.Figure(data=[go.Table(
    header=dict(values=['Prov', 'Kategori', 'Jenis Barang', 'Sum of Qty']),
    cells=dict(values=[table_data['prov'], table_data['kategori'], table_data['jenis_barang'], table_data['qty']])
)])

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Interactive Dashboard with Plotly and Dash"),

    html.H2("Line Chart: Pendapatan Total vs. Bulan"),
    dcc.Graph(figure=line_chart),

    html.H2("Summary of Line Chart"),
    html.Table([
        html.Tr([html.Th('High Point (Pend Total)'), html.Th('Low Point (Pend Total)')]),
        html.Tr([html.Td(f'Bulan: {max_point["bulan"].values[0]}'), html.Td(f'Bulan: {min_point["bulan"].values[0]}')]),
        html.Tr([html.Td(f'Pend Total: {max_point["pend_total"].values[0]}'), html.Td(f'Pend Total: {min_point["pend_total"].values[0]}')]),
    ]),

    html.H2("Pie Chart: Sum of Qty by Diskon"),
    dcc.Graph(figure=diskon_qty_pie_chart),

    html.H3(f"The diskon with the largest sum of qty: {largest_qty_diskon}"),

    html.H2("Pie Chart: Sum of Qty by Jenis Penjualan"),
    dcc.Graph(figure=jenis_penjualan_qty_pie_chart),

    html.H3(f"The jenis_penjualan with the largest sum of qty: {largest_qty_jenis_penjualan}"),

    html.H2("Dual Combination Chart: Barang Jual and Barang Prod"),
    dcc.Graph(figure=combination_chart),

    html.H2("Table: Sum of Qty by Prov, Kategori, and Jenis Barang"),
    dcc.Graph(figure=table)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
