import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt

st.markdown("""
            
            # Dashboard: Data Science und Visualisierung
            
            Willkommen zu meinem Dashboard auf dem ich im Rahmen meines Studiums im Kurs Data Science und Visualisierung versuche Fragen zu einem Datensatz von Capital BikeShare mithilfe von Diagrammen zu beantworten.
            Über die fünf unterschiedlichen Tabs kann man zwischen den einzelnen Grafiken wechseln, die zugehörige Frage steht jeweils darüber.
            """)

df = pd.read_csv(
    "capitalbikeshare-complete.csv",
    sep=","
    )

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Balkendiagramm", "Balkendiagramm", "Kreisdiagramm", "Streudiagramm", "Liniendiagramm"])

with tab1:
    st.write("# Wie oft treten die unterschiedlichen Wetterbedingungen auf?")
    
    weather_count = df['weather_main'].value_counts()

    weather_count_df = weather_count.reset_index()
    weather_count_df.columns = ['weather_main', 'weather_count']
    
    fig = plt.figure()
    sns.barplot(
        data=weather_count_df,
        x="weather_count",
        y="weather_main",
        estimator="sum",
        errorbar=None,
        )
    
    plt.xlabel('Anzahl')
    plt.ylabel('Wetterbedingung')
            
    st.pyplot(fig)
    
with tab2:
    st.write("# Bei welchen Wetterbedingungen wurden die meisten Fahrräder ausgeliehen?")
    
    df_renamed = df.rename(columns={'count': 'Anzahl der ausgeliehenen Räder pro Stunde', 'weather_main': 'Wetterbedingung'})
    
    st.bar_chart(
        data=df_renamed,
        x="Anzahl der ausgeliehenen Räder pro Stunde",
        y="Wetterbedingung",
        width=0, height=500,
        use_container_width=True,
        )
    
with tab3:
    st.write("# Werden am Wochenende oder an Werktagen mehr Fahrräder ausgeliehen?")
    
    count_by_workday = df.groupby('workingday')['count'].sum()
    
    custom_labels = count_by_workday.index.map({0: 'Wochenende', 1: 'Werktag'})

    fig = plt.figure()
    wedges, _, autotexts = plt.pie(count_by_workday, labels=custom_labels, colors=['#8eb7e5', '#6e8660'], autopct='', startangle=90)
    plt.title('Anzahl ausgeliehener Leihräder an Werktagen und Wochenenden')
    plt.axis('equal')
    
    for i, autotext in enumerate(autotexts):
        autotext.set_text(f'{count_by_workday.values[i]}')
        autotext.set_color('white')
        
    total_count = count_by_workday.sum()
    
    st.pyplot(fig)
    
    
with tab4:
    st.write("# Wie verhällt sich die gemessene Temperatur gegenüber der geschätzten Temperatur?")
    
    fig = plt.figure(figsize=(5, 5))
    sns.scatterplot(
        data=df,
        x="temp",
        y="feels_like",
        color="#6e8660"
        )

    plt.xlabel('Temperatur in °C')
    plt.ylabel('gefühlte Temperatur in °C:')
    
    st.pyplot(fig)

with tab5:
    st.write("# In welchen Monaten werden die meisten Fahrräder ausgeliehen?")
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    
    df_resampled = df.resample('M').sum()
    
    fig = plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_resampled, x=df_resampled.index, y="count")
    
    plt.xlabel('Datum')
    plt.ylabel('Anzahl Leihräder')
    plt.title('Verliehene Fahrräder pro Monat')
    
    plt.xticks(df_resampled.index, df_resampled.index.strftime('%Y-%m'), rotation=45)
    
    for date in df_resampled.index:
       plt.vlines(date, 0, df_resampled.loc[date, 'count'], color='gray', linestyle='--', alpha=0.5)
    
    st.pyplot(fig)
