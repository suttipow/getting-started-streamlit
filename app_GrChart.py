import streamlit as st  # pip install streamlit
import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly-express
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module






def generate_excel_download_link(df):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    #df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
    #New generate_excel
    df.to_excel(towrite, index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)



def generate_html_download_link(fig):
    # Credit Plotly: https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)


st.set_page_config(page_title='Revenue Plotter')
st.title('Revenue Plotter 📈 data from Revenue Power BI') 
st.subheader('Feed me with your Excel file')

uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file,sheet_name="Export", engine='openpyxl') # Read data as xlsx
    #df = pd.read_csv(uploaded_file)  # Read data as CSV

     # Calculate RevLoss as Downtime multiplied by revPersec
    df["RevLoss"] = df["Downsec"] * df["revenue(THB/SEC)"]

    st.dataframe(df)
    groupby_column = st.selectbox(
        'What would you like to analyse?',
        ('mc_zone','Province', 'SiteCode', 'Ampore','Tumbol', 'ID'),
    )

    # -- GROUP DATAFRAME
    #output_columns = ['Sales', 'Profit']
    output_columns = ['Downsec', 'RevLoss']  # new output
    df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()

    # -- PLOT DATAFRAME
    fig = px.bar(
        df_grouped,
        x=groupby_column,
        y='Downsec',
        color='RevLoss',
        color_continuous_scale=['green', 'yellow', 'red'],
        template='plotly_white',
        title=f'<b>Sales & Profit by {groupby_column}</b>'
    )
    st.plotly_chart(fig)

    # -- DOWNLOAD SECTION
    st.subheader('Downloads:')
    generate_excel_download_link(df_grouped)
    generate_html_download_link(fig)
