import pickle
import src.Corpus
from importlib import reload

reload(src.Corpus)

# Ouverture du fichier, puis lecture avec pickle
with open("../test_data/id2doc.pkl", "rb") as f:
    id2doc = pickle.load(f)

# Ouverture du fichier, puis lecture avec pickle
with open("../test_data/id2aut.pkl", "rb") as f:
    id2aut = pickle.load(f)


corpus = src.Corpus.Corpus("Space",id2aut,id2doc)
import pandas as pd
dfDocs = corpus.get_id2doc_DF()

dfReddit = dfDocs[dfDocs['Type']=='Reddit']
dfArxiv = dfDocs[dfDocs['Type']=='Arxiv']

#print(corpus.search("algebra"))
#print(corpus.concorde("algebra",5))
print(corpus.matrice())
print(corpus.recherche(["space","new"]))


dictest=corpus.recherche(["space","new"])

    
'''dfReddit['score'] = dfReddit['Nom'].apply(lambda x:dictest[x])
dfReddit = dfReddit.sort_values('score',ascending=False)

dfArxiv['score'] = dfArxiv['Nom'].apply(lambda x:dictest[x])
dfArxiv = dfArxiv.sort_values('score',ascending=False)'''

listeAuteurReddit = dfReddit['Auteur'].unique()
listeAuteurArxiv = dfArxiv['Auteur'].unique()

from dash import Dash, dash_table,dcc,Input,callback_context
from dash import html
import pandas as pd
from dash.dependencies import Input, Output,State

app = Dash(__name__)
from dash import html
    
app.layout = html.Div([
html.Div([
dcc.Input(id='txtSearch',type='text',placeholder='Saisir les mots clés...',style={'margin':'0 auto','display':'block','bottom':'100px'}),
dcc.Dropdown(listeAuteurReddit,id='cbAuteurLeft',style={'width':'100px'}),
dcc.Dropdown(listeAuteurArxiv,id='cbAuteurRight',style={'width':'100px'}),
html.Button('Rechercher', id='btnFilterLeft', n_clicks=None),
html.Button('Rechercher', id='btnFilterRight', n_clicks=None),
],id="divSearch", style={'float':'top','width':'100%','height':'10%','border-style':'solid'}),
html.Div([
dash_table.DataTable(
id='tableReddit',page_size=5,
data=dfReddit.to_dict('records'),     #the contents of the table
columns=[
    {'id': 'Id', 'name': 'ID'},
    {'id': 'Nom', 'name': 'Titre'},
    {'id': 'Auteur', 'name': 'Auteur'},
    {'id': 'Date', 'name': 'Date'},
    {'id': 'URL', 'name': 'URL'},
    {'id': 'Textabrv', 'name': 'Textabrv'},
],style_cell={"width":"5px",'minWidth':'5px','maxWidth':'5px'}),html.Div(id='divDetailsLeft',style={'display':'none','float':'left','width':'49.5%','height':'45%','left':'100px'})],id="divLeft",style={'z-index':'0','float':'left','width':'49.5%','height':'45%'}),
html.Div([
dash_table.DataTable(
id='tableArxiv',page_size=5,
data=dfArxiv.to_dict('records'),     #the contents of the table
columns=[
    {'id': 'Id', 'name': 'ID'},
    {'id': 'Nom', 'name': 'Titre'},
    {'id': 'Auteur', 'name': 'Auteur' },
    {'id': 'Date', 'name': 'Date'},
    {'id': 'URL', 'name': 'URL'},
    {'id': 'Textabrv', 'name': 'abreviatedText'},
],style_cell={"width":"5px",'minWidth':'5px','maxWidth':'5px'}),html.Div(id='divDetailsRight',style={'display':'block','float':'right','width':'49.5%','height':'45%','right':'100px'})],id="divRight",style={'float':'right','width':'49.5%','height':'90%',"display":"block"})])
@app.callback(
    Output('tableReddit', 'data'),
    State('cbAuteurLeft', 'value'),
    State('txtSearch', 'value'),
    Input('btnFilterLeft', 'n_clicks'),
)
def callback_func(cbAuteur_value,keywords,clicks):
    df_filtered = dfReddit.copy()
    if cbAuteur_value:
        df_filtered = dfReddit[dfReddit['Auteur'].eq(cbAuteur_value)]
    if keywords:
        print('---------------------',keywords)
        keywords_clean = corpus.nettoyer_texte(keywords)
        arr_keywords=keywords_clean.split(" ")
        dictest=corpus.recherche(arr_keywords)
        df_filtered['score'] = df_filtered['Nom'].apply(lambda x:dictest[x])
        dfReddit['score']=dfReddit['Nom'].apply(lambda x:dictest[x])
        df_filtered = df_filtered.sort_values('score',ascending=False)
        if cbAuteur_value:
            df_filtered = dfReddit[dfReddit['Auteur'].eq(cbAuteur_value)]
    
    return df_filtered.to_dict(orient='records')
        


@app.callback(
    Output('tableArxiv', 'data'),
    State('cbAuteurRight', 'value'),
    State('txtSearch', 'value'),
    Input('btnFilterRight', 'n_clicks')
)
def callback_func_2(cbAuteur_value,keywords,clicks):
    df_filtered = dfArxiv.copy()
    if cbAuteur_value:
        df_filtered = dfArxiv[dfArxiv['Auteur'].eq(cbAuteur_value)]
    if keywords:
        print('---------------------',keywords)
        keywords_clean = corpus.nettoyer_texte(keywords)
        arr_keywords=keywords_clean.split(" ")
        dictest=corpus.recherche(arr_keywords)
        df_filtered['score'] = df_filtered['Nom'].apply(lambda x:dictest[x])
        dfArxiv['score']=dfArxiv['Nom'].apply(lambda x:dictest[x])
        df_filtered = df_filtered.sort_values('score',ascending=False)
        if cbAuteur_value:
            df_filtered = dfArxiv[dfArxiv['Auteur'].eq(cbAuteur_value)]
    
    return df_filtered.to_dict(orient='records')


@app.callback(
    [Output("divDetailsLeft", "children"),
     Output("divDetailsLeft", "style")],
    Input('tableReddit', 'active_cell'),
    State('tableReddit', 'data')
)
def callback_func_3(active_cell,data):  
    return_value=()
    if active_cell:
        row = active_cell['row']
        Id=data[row]['Id']
        if dfReddit[dfReddit['Id'].eq(Id)]['score'].values[0]<=0.25:
            color = 'rgb(176,242,182)'
        elif dfReddit[dfReddit['Id'].eq(Id)]['score'].values[0]<=0.5:
            color = 'rgb(104,230,116)'
        else:
            color = 'rgb(47,221,63)'   
        #print(Id)
        #print(dfSpaceReddit[dfSpaceReddit['Id'].eq(Id)]['Text'])
        return_value = html.Div([html.B('Score : '),html.Label(children=[str(dfReddit[dfReddit['Id'].eq(Id)]['score'].values[0])],style={'background-color':color}),html.Br(),html.B('Full text : '),dcc.Textarea(style={'font-size':'20px'},value=dfReddit[dfReddit['Id'].eq(Id)]['Text'],rows=10,cols=30)]),{'display':'block'}
    return return_value 

@app.callback(
    [Output("divDetailsRight", "children"),
     Output("divDetailsRight", "style")],
    Input('tableArxiv', 'active_cell'),
    State('tableArxiv', 'data')
)
def callback_func_4(active_cell,data):  
    return_value=()
    if active_cell:
        row = active_cell['row']
        Id=data[row]['Id']
        print(Id)
        if dfArxiv[dfArxiv['Id'].eq(Id)]['score'].values[0]<=0.25:
            color = 'rgb(176,242,182)'
        elif dfArxiv[dfArxiv['Id'].eq(Id)]['score'].values[0]<=0.5:
            color = 'rgb(104,230,116)'
        else:
            color = 'rgb(47,221,63)'            
        #print(Id)
        #print(dfSpaceReddit[dfSpaceReddit['Id'].eq(Id)]['Text'])
        return_value = html.Div([html.B('Score : '),html.Label(children=[str(dfArxiv[dfArxiv['Id'].eq(Id)]['score'].values[0])],style={'background-color':color}),html.Br(),html.B('Full text : '),html.Br(),dcc.Textarea(style={'font-size':'20px'},value=dfArxiv[dfArxiv['Id'].eq(Id)]['Text'],rows=10,cols=30)]),{'display':'block'}
    return return_value 
"""
@app.callback(
    [Output("divDetailsLeft", "children"),
     Output("divDetailsLeft", "style"),
     Output("divLeft","style")],
    [Input('tableReddit', 'active_cell'),
     Input('btnBackLeft', 'n_clicks')],
    State('tableReddit', 'data')
)

def callback_func_3(active_cell,clicks,data):  
    return_value=()
    global goBack
    if not(goBack):
        if active_cell:
            row = active_cell['row']
            Id=data[row]['Id']
            #print(Id)
            #print(dfSpaceReddit[dfSpaceReddit['Id'].eq(Id)]['Text'])
            return_value = html.Div([html.Button('Retour aux données', id='btnBackLeft', n_clicks=0,style={'float':'right','position':'absolute'}),html.B('Full text : '),html.Br(),dcc.Textarea(style={'font-size':'20px'},value=dfSpaceReddit[dfSpaceReddit['Id'].eq(Id)]['Text'],rows=10,cols=30)]),{'display':'block'},{'display':'none'}
            goBack=True
        else :
            return_value='','',''
    else:
        return_value = '',{'display':'none','float':'left','width':'49.5%','height':'100%','left':'100px'},{'display':'block','float':'left','width':'49.5%','height':'100%','left':'100px'}
        goBack=False
    print(return_value)
    return return_value 
"""

if __name__ == '__main__':
    app.run_server()
