import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import plotly.express as px 
import plotly.graph_objects as go
import pickle

df=pd.read_csv('ODI.csv')
df1=df.head(10)

df2=pd.read_csv('Countries_data.csv')



if "center" not in st.session_state:
    layout = "wide"
else:
    layout = "centered" if st.session_state.center else "wide"

st.set_page_config(layout=layout)

st.checkbox(
    "Viewing on a mobile?", key="center", value=st.session_state.get("center", False)
)

def ChangeWidgetFontSize(wgt_txt, wch_font_size = '12px'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        { elements[i].style.fontSize='""" + wch_font_size + """';} } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)

#graph1
team1=df.Team_1.value_counts()
team2=df.Team_2.value_counts()
teams=team1+team2
teams['Africa XI']=team1['Africa XI']
teams['ICC World XI']=team2['ICC World XI']
teams=pd.DataFrame(teams)
teams['count']=teams
teams['Teams']=teams.index
teams.reset_index(drop=True,inplace=True)
teams=teams.sort_values('count',ascending=False)
fig1= px.bar(teams, x="Teams",y="count",color='count',color_continuous_scale='Viridis') 
fig1.update_layout(
    yaxis_title="No of Matches",
    xaxis_title="Teams"
)


#graph2
By=[]
runs=[]
wickets=[]
for i in df['Margin']:
    
    margin=i.split(' ')
    
    if(len(margin)==2 and (margin[1]=='runs' or margin[1]=='run')):
        By.append('Defending')
        runs.append(int(margin[0]))
    elif(len(margin)==2 and (margin[1]=='wickets' or margin[1]=='wicket')):
        By.append('Chasing')
        wickets.append(int(margin[0]))
    else:
        By.append('Tied')

df['Wonby']=By
fig2=px.bar(df,x='Wonby',color='Wonby', color_continuous_scale='Viridis')



#graph3
year=[]
for i in df['Match Date']:
    data=i.split(' ')
    year.append(int(data[-1]))
data_counts = pd.Series(year).value_counts().reset_index()
data_counts.columns = ['value', 'count']
fig3=px.bar(data_counts,x='value',y='count',color='count',color_continuous_scale='Viridis')




#Graph4
grounds=df['Ground'].value_counts()
grounds=pd.DataFrame(grounds)
grounds['Grounds']=grounds.index
grounds.reset_index(drop=True,inplace=True)
grounds=grounds[:25]
fig4= px.bar(grounds, x="Grounds", y="count",color='count',color_continuous_scale='Viridis') 



#graph5
winners=df['Winner'].value_counts()
fig5=px.bar(y=df['Winner'].value_counts(),x=df['Winner'].unique(),color=df['Winner'].value_counts(),color_continuous_scale='Viridis')
fig5.update_layout(
    yaxis_title="No of Matches",
    xaxis_title="Country"
)

#graph6
top_countries=['Australia', 'Bangladesh', 'England', 'India', 'New Zealand',
       'Pakistan', 'South Africa', 'Sri Lanka', 'West Indies', 'Zimbabwe']


matches_country=[]
countr=top_countries
for i in countr:
    list=df2[(df2['Winner']==i)& (df2['Countries'].isin(top_countries)) ]['Countries'].value_counts()
    matches_country.append(list)

for i,j in enumerate(matches_country):
    matches_country[i]=matches_country[i].sort_index()

games_played=[]
for i in matches_country:
    games_played.append(i.values)

x_countries=matches_country[0].index
y_countries=matches_country[0].index

fig6 = go.Figure(data=go.Heatmap(
    z=games_played,
    x=x_countries,
    y=y_countries,
    colorscale="Viridis",  
    colorbar=dict(title="Matches Won")
))


#Model prerequisites

teams=['Australia','India','West Indies', 'New Zealand','South Africa',
       'England', 'Bangladesh', 'Sri Lanka', 'Pakistan', 
       'Afghanistan']

cities=['Visakhapatnam', 'Fatullah', 'Hyderabad', 'Antigua', 'Hamilton',
       'Jaipur', 'Christchurch', 'Abu Dhabi', 'Mirpur', 'St Kitts',
       'St Lucia', 'Colombo', 'Guyana', 'Kanpur', 'Pune', 'Karachi',
       'Trinidad', 'Southampton', 'Wellington', 'Port Elizabeth',
       'Lahore', 'Melbourne', 'Barbados', 'Nelson', 'Pallekele',
       'Vadodara', 'Cape Town', 'Manchester', 'Nottingham', 'Rangiri',
       'Perth', 'London', 'Chennai', 'Cuttack', 'Rajkot', 'Centurion',
       'Hambantota', 'Jamaica', 'Indore', 'Dubai', 'Johannesburg',
       'Sydney', 'Napier', 'Mount Maunganui', 'Dublin', 'Gwalior',
       'Birmingham', 'Bangalore', 'Chandigarh', 'Delhi', 'Multan',
       'Auckland', 'Nagpur', 'Hobart', 'Leeds', 'Bristol', 'Grenada',
       'Lucknow', 'Chester-le-Street', 'Kuala Lumpur', 'Mumbai',
       'Adelaide', 'Dhaka', 'Ranchi', 'Harare', 'Canberra', 'Cardiff',
       'Durban', 'Sharjah', 'Taunton', 'Brisbane', 'Kimberley',
       'Bridgetown', 'Kolkata', 'Guwahati', 'Chittagong', 'Queenstown',
       'Faisalabad', 'St Vincent', 'Ahmedabad', 'Dunedin', 'Bengaluru',
       'Dominica', 'Rawalpindi', 'Margao', 'Belfast', 'Kochi',
       'Bloemfontein', 'East London', 'Potchefstroom']

wickets=[10,9,8,7,6,5,4,3,2,1]

columns=['batting_team', 'bowling_team', 'city', 'current_score', 'balls_left',
       'wickets_left', 'last_five']

#model
model=pickle.load(open('pipe2.pkl','rb'))

st.title("Evolution of Cricket :cricket_bat_and_ball:")

nav=st.sidebar.radio(':blue[Navigation]',['Home','Score Predictor'])
ChangeWidgetFontSize('Navigation', '32px')

if nav == 'Home':
    
    st.header(':blue[Home]')
    st.image('pxfuel.jpg',width=650)

    st.write("")
    st.write("")

    st.subheader(":blue[Sample Data]")
    if st.checkbox('Show Sample Data'):
        st.table(df2.head(10))
    
    st.write("")
    st.write("")

    st.header('Graphs')
    

    st.subheader(':blue[Number of Matches played by each team]')
    st.write("This graph represents number of matches played by each team till 2023.")
    st.plotly_chart(fig1,use_container_width=True)
    st.write("Since the inception of ODIs in 1971, India has played the highest number of matches (1029), closely followed by Australia (978) and Pakistan (953). These cricketing powerhouses have consistently been at the forefront of the One Day International format, contributing to the sport's rich history with their remarkable performances and passionate fan bases.")

    st.write("")
    st.write("")

    st.subheader(':blue[Results]')
    st.write("This graph illustrates the distribution of matches won based on different scenarios: chasing, defending, or resulting in a tie.")
    st.plotly_chart(fig2,use_container_width=True)
    st.write("The gap between the number of matches won by chasing (2213) and defending (2157) is remarkably narrow. Notably, an astonishing 208 matches were tied from 1971 up to the present day. This highlights the highly competitive nature of cricket, where teams have shown almost equal prowess in both chasing and defending, resulting in thrilling encounters that have occasionally ended in draws.")

    st.write("")
    st.write("")

    st.subheader(':blue[Top Venues]')
    st.write('This graph represents the number of matches held in each venue.')
    st.plotly_chart(fig4,use_container_width=True)
    st.write("Among various cricket teams, Australia and India stand out for having played the highest number of matches. Surprisingly, the venue that hosted the most matches is not in either of these countries, but rather in Sharjah, with a staggering 244 matches held there. Harare follows next with 174 matches, while Sydney, Melbourne, and Columbia secure their places in the list with 160, 150, and 138 matches hosted, respectively")

    st.write("")
    st.write("")
    st.write("")
    st.write("")

    st.subheader(':blue[Number of Matches played in each year]')
    st.write("This chart represents the number of international matches conducted each year.")
    st.plotly_chart(fig3,use_container_width=True)


    st.write("")
    st.write("")
    st.write("")

    st.subheader(':blue[Global Team Win Distribution ]')
    st.write("This chart represents number of matches won by a team in each country.")
    st.plotly_chart(fig6,use_container_width=True)

    st.write("")
    st.write("")
    st.write("")

    st.subheader(':blue[Most wins]')
    st.write("This chart represents total number of wins by a team till 2023.")
    st.plotly_chart(fig5,use_container_width=True)
    st.write("In the realm of One Day Internationals, Australia stands out as the dominant force, having secured the highest number of victories (594). Trailing closely behind are India (539), Pakistan (503), West Indies (411), and South Africa (399). ")

if nav=='Score Predictor':
    st.header(':blue[Score Predictor]')

    st.write(":blue[**NOTE**] : Please choose the follwing options which are likely to happen in a real match situation to get a better prediction from the model.")

    batting_team = st.selectbox('Select Batting Team:', teams)
    teams2 = [x for x in teams if x != batting_team]
    bowling_team = st.selectbox('Select Bowling Team:',teams2)
    city = st.selectbox('Select Venue:',cities)
    current_score = st.number_input("Enter the Current Score:", min_value=0, max_value=440, value=0)
    balls_left=st.number_input ("Enter the number of Balls left in the Match:",min_value=0,max_value=300,value=300)
    wickets_left = st.selectbox('Select The number of wickets left:',wickets)
    last_five_overs= st.number_input("Enter the runs made in Last 5 Overs:", min_value=0, max_value=100, value=0)


    inputs=[[batting_team,bowling_team,city,int(current_score),int(balls_left),int(wickets_left),int(last_five_overs)]]

    x=pd.DataFrame(inputs,columns=columns)

    result=model.predict(x)

    if st.button('Predict'):
        if int(result)<current_score:
            st.write("The model predicts the score to be {}, which is less than the current score as it has been trained on many instances in which the predicted score was which the batting team could manage and the input given might be an exceptional case.".format(result))
        st.success('The Predicted Score is {}'.format(result))
        
