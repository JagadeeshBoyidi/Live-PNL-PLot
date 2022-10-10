import os
import pandas as pd
import time
import datetime
import plotly.graph_objects as go
from telegram import Bot
from plotly.subplots import make_subplots



def send_image_bot():
    bot = Bot(token='2109482112343214324:alkfjaslkfjasfoiwar')
    return bot
       
def chart_pnl():
    
    #Reading the pnl stored in the logs folder with the current date
    #csv file contains 4 columns in a sequence "timestamp", "pnl","pts","roc"
    df = pd.read_csv("logs"+"//"+'ts_pnl_'+str(datetime.datetime.now().date())+'.csv', header=None,error_bad_lines=False,engine='python')
    df = df.dropna()    
    df =df[pd.to_numeric(df[2], errors='coerce').notnull()]    
    df.rename(columns = {0:"timestamp",1:"pnl",2:"pts",3:"roc"},inplace = True)
    
    df['pnl']= df.pnl.apply(lambda x:float(x))
    df['pts'] = df.pts.apply(lambda x:float(x))
    df['roc'] = df.roc.apply(lambda x:float(x))
    
    
    #removing the pnl values that contains zero
    
    df = df[df['pnl'] !=0]

    
    df['timestamp']= df['timestamp'].apply(lambda x:datetime.time(int(x[:2]),int(x[3:5])))
    df['time'] = df['timestamp'].apply(lambda x: datetime.datetime.combine(datetime.datetime.now().date(), x) )
    df.index = pd.to_datetime(df.time, unit='s')
    
    #taking last pnl stored for every minute
    df = df[~df.index.duplicated(keep='last')]
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add traces
    fig.add_trace(
        go.Scatter(x=df.index, y=df.pts.values,name = 'Points', line=dict( width=3)),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df.roc.values, name = 'Roc',line=dict( width=3)),
        secondary_y=True,
    )
    
    
    fig.add_annotation(
            x=df.index[-1],
            y=df.pts[-1],
             text = "  "+str(round(df.pts[-1],1)),
             secondary_y=False,
            showarrow=True)
    
    
    # Add figure title
    fig.update_layout(
        title_text="Ts Stats",
        font=dict(
        family="Courier New, monospace",
        size=33,
        color="RebeccaPurple"
    ))
    
    # Set x-axis title
    fig.update_xaxes(title_text="time")
    
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Points</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Roc</b>", secondary_y=True)
    
    # fig.show()
    #storing the files in "charts" folder
    try:
        os.makedirs("charts"+'//'+str(datetime.datetime.now().date()))
    except FileExistsError:
        pass
        
        
    chart_name = "charts"+'//'+str(datetime.datetime.now().date())+'//'+str(time.time()).split('.')[0] +"-"+str('rs_pnl')+'.png'
    fig.write_image(chart_name,width = 2400, height = 1500)
    
    #bot that sends image to telegram
    send_image_bot().send_photo(chat_id='@abc_1234',  photo=open(chart_name, "rb"))
    
    
  