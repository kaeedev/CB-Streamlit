import streamlit as st 
import pandas as pd
import numpy as np #Para generar numeros aleatorios
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time
#Elemento de cacheo. Para que guarde los resultados y no recargue constantemente aunque le pasemos las mismas opciones. Se suele usar para
#elementos que generan datos
@st.cache_data
#Elementos de Dataframe (Una tabla)
def get_df(high_limit, low_limit, x_size, y_size):
    st.session_state['df'] = pd.DataFrame(
        np.random.randint( #Nos va a generar una lista de 10 filas y 10 columnas de numeros randoms
            low = low_limit, #Minimo numero el -10
            high = high_limit, #Maximo numero el 10
            size = (x_size, y_size), #La tabla de 10 x 10
        ),
        columns = ('col %d' % i for i in range(y_size)) #Esto genera 10 columnas que se llamaran col 1, col 2, col 3...
    )

    return st.session_state['df']

#Configuracion inicial de la apgina. Debe ir siempre lo primero de todo antes de que se llame a algo
st.set_page_config(
    page_title = 'First time in Streamlit', 
    page_icon = '👑',
    layout='wide', #Layout de la pagina
    initial_sidebar_state='expanded',
    menu_items={
        'Get help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': 'https://www.extremelycoolapp.com/bug',
        'About': '#This is a header. Yhis is a *extremely* cool app!'
    }

)
#Elemento de sesion. Guardaremos en la sesion nuestro df. Ahora en todos los sitios donde nos referimos a df, debemos sustituirlo por el
#st.session_state['df']
if 'df' not in st.session_state:
    st.session_state['df'] = None


#Elemento de input
#Un chat. Si no queremos q se ponga en un lado, quitamos el sidebar
s = st.sidebar.chat_input(
    placeholder = 'Your message'
)
if s:
    st.sidebar.success(s)

def page_1():
    #Elemento de media. Aparte de imagenes tambien se pueden incrustar audios, videos, etc

    st.image('https://cdn.prod.website-files.com/63c2c7b1f3d9c51c32335fb0/664c5634a1dfc7c6526459ec_Conquer-Blocks-logo.png')
    #Elementos de texto

    #Para poner un titulo
    st.title('Streamlit basics')
    #Title es el mayor tamaño, luego tenemos header, subheader...

    #Para poner strings de textos. Se le puede inyectar HTML
    st.markdown('A brief projects on streamlit widgets :sunglasses:')

    #Para dividir el texto con una barra
    st.divider()

#Elemento de navegacion. Creamos una pagina nueva
def page_2():
    #Elementos de input

    #Para hacer un boton para generar el dataframe al pulsarlo
    #generate_df = st.button('Generate df')
    #if generate_df:
    #    df = get_df()

    #Podemos hacer lo mismo con un checkbox, que se mantiene a true aunque recarguemos, no como el boton
    generate_df = st.checkbox('Generate df')
    
    if generate_df:

        #Elemento de layout expander, que es agrupar dentro de una caja los datos que queramos y podemos expandirlo o ocultarlo para que quede todo
        #mucho mas compacto
        with st.expander('Data'):
        #Elemento de layout para poner los widgets en columnas
            col1, col2, col3 = st.columns([2,6,2]) #Estos valores son lo q ocupara cada columna

            #Elemento de input
            #Un cuadrado de texto para insertar un numero y definir el tamaño del eje x de nuestra tabla (dataframe)
            with col1:
                #Elemento de formulario
                with st.form('computed_form'):
                    #Elemento de layout empty. Deja un hueco vacio para que luego al interaccionar con otro codigo, lo coloque en esta posicion. Por ejemplo un write cuando se genere el dataframe, que aparezca aqui un mensaje
                    empty_widget = st.empty()
                    x_size = st.number_input(
                        'X Size',
                        min_value = 1, #valor minimo
                        max_value = 4000, #valor maximo
                        value=10, #valor inicial
                        step= 1 #Step es los saltos que da de numero en numero, en este caso va de 1 en 1 pero puede ser de 4 en 4 etc
                    )

                    y_size = st.number_input(
                        'Y Size',
                        min_value = 1, #valor minimo
                        max_value = 4000, #valor maximo
                        value=10, #valor inicial
                        step= 1 #Step es los saltos que da de numero en numero, en este caso va de 1 en 1 pero puede ser de 4 en 4 etc
                    )

                    #Elementos de input
                    #Sliders para manejar el limite inferior o superior de los numeros que pueden salir en la tabla
                    low_limit = st.slider(
                        'Low limit',
                        min_value = -1000, #valor minimo
                        max_value = 1000, #valor maximo
                        value=-10, #valor inicial
                        step= 1 #Step es los saltos que da de numero en numero, en este caso va de 1 en 1 pero puede ser de 4 en 4 etc
                    )

                    high_limit = st.slider(
                        'High limit',
                        min_value = -1000, #valor minimo
                        max_value = 1000, #valor maximo
                        value=10, #valor inicial
                        step= 1 #Step es los saltos que da de numero en numero, en este caso va de 1 en 1 pero puede ser de 4 en 4 etc
                    )
                    submitted = st.form_submit_button('Submit')
                    #Boton del formulario
                if submitted:
                    st.session_state['df'] = get_df(high_limit, low_limit, x_size, y_size)
                else:
                    st.info('Click on "Submit" for generate the datas')

            with col2: 
                if st.session_state['df'] is not None:
                    #Elemento de status para que genere una ruedecita como de espera mientras carga algo
                    with st.spinner('Generating dataframe...'):
                        time.sleep(0.5)
                        st.session_state['df'] = get_df(high_limit, low_limit, x_size, y_size)
                        st.dataframe(st.session_state['df'])
                        empty_widget.write('Dataframe dimensions %d x %d' % (st.session_state['df'].shape)) #Llamamos al empty para que coloque un mensaje con las dimensiones del df

            #Elemento de input que es un boton para descargar datos. En este caso descargamos el dataframe
            with col3:
                if st.session_state['df'] is not None:
                    download_button = st.download_button(
                        label = 'Download df', #Titulo
                        data = st.session_state['df'].to_csv(), #El dataframe y lo convertimos a csv
                        file_name='My dataframe.csv' #El nombre del archivo al descargar
                    )
                else:
                    st.warning('Please generate the Dataframe first and you can download')

        #Elemento de layout expander, que es agrupar dentro de una caja los datos que queramos y podemos expandirlo o ocultarlo para que quede todo
        #mucho mas compacto
        with st.expander('Metrics'):
            
            metrics_selection = st.multiselect(
                label = 'Select metrics to show',
                options = ['Max', 'Min', 'Mean'],
                placeholder = 'Choose an option',
            )
            if st.session_state['df'] is not None:
            #Podemos hacer una metrica de valores a partir de un dataframe como por ejemplo averiguar el numero mas alto. Se hace con metric.
                df_max = st.session_state['df'].max().max() #encontrar el maximo valor
                df_min = st.session_state['df'].min().min() #encontrar el minimo valor
                df_mean = st.session_state['df'].mean().mean() #encontrar el valor medio

                if 'Max' in metrics_selection:
                    st.metric(
                        'Max value', #El label, el titulo
                        df_max, #El valor
                        delta = 'Max', #Por defecto
                        delta_color= 'normal', #Por defecto
                        help = 'The max value of the dataframe' #Un mensaje de ayuda para cuando se pase el raton por encima

                    )

                if 'Min' in metrics_selection:
                    st.metric(
                        'Min value', #El label, el titulo
                        df_min, #El valor
                        delta = 'Min', #Para ponerle un texto debajo, suele ser para indicar ganancias o perdidas o positivo o negativo con una flecha apra arriba o para abajo
                        delta_color= 'inverse', #Para cambiar el color del mensaje, puede ser verde o rojo. Normal o Inverse
                        help = 'The min value of the dataframe' #Un mensaje de ayuda para cuando se pase el raton por encima

                    )
                if 'Mean' in metrics_selection:
                    st.metric(
                    'Mean value', #El label, el titulo
                    df_mean, #El valor
                    delta = None, #Por defecto
                    delta_color= 'normal', #Por defecto
                    help = 'The mean value of the dataframe' #Un mensaje de ayuda para cuando se pase el raton por encima

                )

        #Podemos imprimir tambien un dataframe sin el write
        # st.dataframe(df)

        #Elemento de layout expander, que es agrupar dentro de una caja los datos que queramos y podemos expandirlo o ocultarlo para que quede todo
        #mucho mas compacto
        with st.expander('Plots'):

            #Elemento de input
            #Una lista para seleccionar solamente una de las opciones
            #plot_type = st.radio(
                #label = 'Select plot library',
                #options = ['Matplotlib', 'Plotly2D', 'Plotly 3D']
            #)

            #Un selectbox que es como el multiselect pero solo podemos seleccionar una opcion. Es un desplegable
            colorscale = st.selectbox(
                'Choose color',
                options = [
                    'viridis',
                    'cividis',
                    'inferno',
                    'magma',
                    'plasma',
                    'Greys'
                ]
            )

            #Elemento de layout para que seleccionar mediante pestañitas lo que queramos ver en vez de hacerlo con radio buttons
            tab1, tab2, tab3 = st.tabs(['Matplotlib', 'Plotly2D', 'Plotly 3D'])
            #Elementos de graficos

            #Para un mapa de alturas con pyplot. Debemos definir una figura y un contorno que sera los valores de un dataframe
            #Debemos instalar matplotlib y pyplot
            if st.session_state['df'] is not None:
                with tab1:
                    fig1 = plt.figure()
                    contour = plt.contour(
                        st.session_state['df'],
                        cmap = colorscale #Para cambiar el color con el selectbox en matplotlib
                    )
                    plt.colorbar(contour) #Para un indice con las alturas del mapa
                    st.pyplot(fig1)

                #Para otro mapa de alturas con plotly. Es mas moderna y tiene mas opciones q pyplot. Hay q instalar plotly e importarlo
                with tab2:
                    fig2 = go.Figure(
                        data = 
                        go.Contour(
                            z = st.session_state['df'], #Suele ser z por el eje z
                            colorscale = colorscale  #Para cambiar el color con el selectbox en plotly
                        )
                    )
                    st.plotly_chart(fig2)


                #En este plotly usamos surface en vez de contour para que sean alturas en 3d
                with tab3:
                    fig3 = go.Figure(
                        data = 
                        go.Surface(
                            z = st.session_state['df'], #Suele ser z por el eje z
                            colorscale = colorscale
                        )
                    )
                    st.plotly_chart(fig3)
    else:
        st.info('Click on "Generate Dataframe" to see the datas')


pg = st.navigation([
    st.Page(page_1, title='Intro', icon='🏡'),
    st.Page(page_2, title='Data & Plots', icon='💹'),
])
pg.run()

#Esta es la forma de dividirlo en paginas, pero si queremos dividir las paginas en capitulos utilizaremos corchetes para hacer diccionarios:

#pg = st.navegation(
#    {
#         'Home':[st.Page(page_1, title='Intro', icon='🏡')],
#        'Data':[st.Page(page_2, title='Data & Plots', icon='💹')],
#    }
#)
#pg.run()
#De esta forma las paginas estaran divididas en home, en data...