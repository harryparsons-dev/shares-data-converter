# %%
import pandas as pd
import weasyprint
import webbrowser
import datetime
import os
import yfinance as yf
import math
import matplotlib.pyplot as plt


def highlight_values(x):
   if x < 0:
      return 'color: red'
   else:
      return 'color: black'

def scan_for_csv_files(directory):
    """Scans a directory for CSV files and returns their paths.

    Args:
        directory: The directory to scan.

    Returns:
        A list of paths to CSV files found in the directory.
    """

    csv_files = []
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            csv_file_path = os.path.join(directory, file)
            csv_files.append(csv_file_path)
    return csv_files

files = scan_for_csv_files(os.getcwd())
count = 0

def getSector(ticker):
    try:
        x = str(ticker)
        sym = ""
        if ((str(ticker))[-1:]) == ".":
            sym += str(ticker) + "L"
        else:
            sym += str(ticker) + ".L"
        stock = yf.Ticker(sym)
        stock= stock.info
        return stock['sector']

    except:
        pass







for csv in files:



    df = pd.read_csv(csv)
    pd.set_option('display.width', 300)




    df.columns = df.columns.str.strip('\ufeff')
    totals = df.tail(2)

    df.drop(df.tail(2).index,inplace=True)




    df["Gain/Loss %"] = df["Gain/Loss %"].str.rstrip("%").astype('float')

    df["Day Gain/Loss"] = df["Day Gain/Loss"].str.rstrip("£")
    sectors = {}
    # Iterating through the column using iteritems
    for column_name, column_data in df.items():
        if column_name == 'Symbol':

            for value in column_data:
                if not pd.isna(value):
                    sector  = getSector(str(value))

                    if sector in sectors:
                        sectors[sector] +=1
                    else:
                        sectors[sector] = 1



    print(sectors)
    labels = []
    size = []
    for sector, count in sectors.items():
        labels.append(sector)
        size.append(size)


    plt.pie(size, labels=labels)
    plt.axis('equal')
    plt.show()
    df =df.sort_values(["Gain/Loss %"], ascending=False)




    df["Gain/Loss %"] = df["Gain/Loss %"].astype(str) + "%"



    result = pd.concat([df,totals])
    result = result.fillna('')

    # result["Day Gain/Loss"] =  result["Day Gain/Loss"].style.applymap(highlight_values)





    HTML_TEMPLATE1 = '''
    <html>
    <head>
    <style>
    @page {
        size: landscape;
        margin: 0in 0in 0in 0in;

    }
    body{
        display:flex;
        flex-direction: row-reverse;
        margin:0;
    }
    div{
        position: relative;

        font-size: 7px;
        width: 10%;
        font-family:  	Courier New;
        padding-top: 10px;

        font-weight: bold;

    }
    table {
        margin-left: 0;
        margin-right: 0;
        margin-top:0;
        font-size:10px;
    }
    table, th, td {
        border: 0.2px solid black;
        border-collapse: collapse;
    }
    th, td {
        padding: 2px;
        text-align: left;
        font-family: Helvetica, Arial, sans-serif;

    }
    table tbody tr:hover {
        background-color: #dddddd;
    }
    table thead th {
        text-align: center;
    }
    .wide {
        width: 90%;
    }
    </style>
    </head>
    <body>
    '''

    HTML_TEMPLATE2 = '''
    </body>
    </html>
    '''


    def to_html_pretty(df, filename='out.html', title=''):
        '''
        Write an entire dataframe to an HTML file
        with nice formatting.
        Thanks to @stackoverflowuser2010 for the
        pretty printer see https://stackoverflow.com/a/47723330/362951
        '''
        ht = ''
        if title != '':
            ht += '<div> %s </div>\n' % title
        ht += df.to_html(classes='wide', escape=False, index=False)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(HTML_TEMPLATE1 + ht + HTML_TEMPLATE2)

    # Pretty print the dataframe as an html table to a file
    intermediate_html = 'intermediate.html'

    x = datetime.datetime.now()
    title = 'Updated: ' + x.strftime('%b') + ' ' + x.strftime('%y')
    # to_html_pretty(result,intermediate_html, title )
    # if you do not want pretty printing, just use pandas:
    # df.to_html(intermediate_html)

    # Convert the html file to a pdf file using weasyprint

    out_pdf= os.path.basename(os.path.normpath(csv)).replace('.csv', '') + '.pdf'
    # weasyprint.HTML(intermediate_html).write_pdf(out_pdf)


    # webbrowser.open_new_tab("/tmp/intermediate.html")

    # weasyprint.HTML('/tmp/intermediate.html').write_pdf('out.pdf')
    # This is the table pretty printer used above:
