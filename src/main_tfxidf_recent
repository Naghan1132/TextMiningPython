import pickle
import Corpus
from importlib import reload

reload(Corpus)

# Ouverture du fichier, puis lecture avec pickle
with open("../test_data/id2doc.pkl", "rb") as f:
    id2doc = pickle.load(f)

# Ouverture du fichier, puis lecture avec pickle
with open("../test_data/id2aut.pkl", "rb") as f:
    id2aut = pickle.load(f)

corpus = Corpus.Corpus("Space",id2aut,id2doc)

sizeVocabReddit = len(corpus.getVocabReddit())
sizeVocabArxiv = len(corpus.getVocabArxiv())
corpus.matrice()
import pandas as pd
dfDocs = corpus.get_id2doc_DF()

dfReddit = dfDocs[dfDocs['Type']=='Reddit']
dfArxiv = dfDocs[dfDocs['Type']=='Arxiv']

from dash import Dash, dash_table,dcc,Input,callback_context
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output,State
import math

componentsStatsArxiv = []
componentsStatsReddit = []
componentsStatsReddit.append(f"Taille du vocabulaire : {len(corpus.vocab)}")
componentsStatsReddit.append(html.Br())
componentsStatsReddit.append(html.Br())
componentsStatsReddit.append(html.Br())

componentsStatsReddit.append("Top 20 des mots les plus utilisés")
componentsStatsReddit.append(html.Br())
componentsStatsReddit.append(html.Br())
dictVoctfxIdf={}
for index, row in corpus.dfTFxIDF.iterrows():
    dictVoctfxIdf[index]=row.sum()
    
for key, value in list(sorted(dictVoctfxIdf.items(),key=lambda x: x[1],reverse=True))[:20]:
    lab=html.Label(key+'=> tfxidf : '+str(round(value,3)))
    componentsStatsReddit.append(lab)
    componentsStatsReddit.append(html.Br())

for key,value in list(sorted(corpus.getVocabArxiv().items(), key=lambda x: x[1]['term frequency']*math.log(len(corpus.id2doc.values())/x[1]['document frequency']), reverse=True))[:20]:
    tfxidf = value['term frequency'] * math.log(len(corpus.id2doc.values())/value['document frequency'])
    lab=html.Label(key+'=>tfxidf: '+str(round(tfxidf,3)))
    componentsStatsArxiv.append(lab)
    componentsStatsArxiv.append(html.Br())
        

        
    

#print(corpus.search("algebra"))
#print(corpus.concorde("algebra",5))
print(corpus.matrice())
print(corpus.recherche(["space","new"]))

dfTFxIdf = corpus.getdfTFxIdf()
arr_text = ["space","new","pasta"]
print(dfTFxIdf.loc['space'][dfReddit[dfReddit['Id'].eq(1)]['Nom']].values[0])
    

dictest=corpus.recherche(["space","new"])

    
'''dfReddit['score'] = dfReddit['Nom'].apply(lambda x:dictest[x])
dfReddit = dfReddit.sort_values('score',ascending=False)

dfArxiv['score'] = dfArxiv['Nom'].apply(lambda x:dictest[x])
dfArxiv = dfArxiv.sort_values('score',ascending=False)'''

listeAuteurReddit = dfReddit['Auteur'].unique()
listeAuteurArxiv = dfArxiv['Auteur'].unique()



app = Dash(__name__)
from dash import html



app.layout = html.Div([dcc.Dropdown(
        id = 'dropdown-to-show_or_hide-element',
        options=[
            {'label': 'Informations générales', 'value': 'on'},
            {'label': 'Détails des corpus par Document', 'value': 'off'}
        ],
        value = 'on'
    ),html.Div(id="divInfos",children=[html.Center(html.H1('Informations générales (utilisez le menu déroulant pour changer de menu)')),html.Div([html.Center([html.H2('Corpus "Space" Reddit'),html.Label("Ce corpus de document contient les 10 premiers documents",style={'font-size':'20px'}),html.Br(),html.Label("en recherchant le mot clé \"Space\" sur Reddit",style={'font-size':'20px'}),html.Br(),html.Br(),html.Label("En voici quelques statistiques :",style={'font-size':'20px'}),html.Div(id="statsReddit",children=componentsStatsReddit)])],style={'float':'left','width':'49.5%','height':'100%','border-right': 'solid 0.5px'}),html.Div([html.Center([html.H2('Corpus "Space" Arxiv'),html.Label("Ce corpus de document contient les 10 premiers documents",style={'font-size':'20px'}),html.Br(),html.Label("en recherchant le mot clé \"Space\" sur Arxiv",style={'font-size':'20px'}),html.Br(),html.Br(),html.Label("En voici quelques statistiques :",style={'font-size':'20px'}),html.Div(id="statsArxiv",children=componentsStatsArxiv)])],style={'float':'right','width':'49.5%','height':'100%','position':'relative'})],style={'z-index':'1','width':'100%','height':'100%','position':'absolute','background-color':'white'}),html.Div(id='mainDocDetails',children=[
html.Div([
dcc.Input(id='txtSearch',type='text',placeholder='Saisir les mots clés...',style={'margin':'0 auto','display':'block','bottom':'100px'}),
dcc.Dropdown(listeAuteurReddit,id='cbAuteurLeft',style={'width':'100px'}),
dcc.Dropdown(listeAuteurArxiv,id='cbAuteurRight',style={'width':'100px'}),
html.Button('Rechercher', id='btnFilterLeft', n_clicks=None),
html.Button('Rechercher', id='btnFilterRight', n_clicks=None),
],id="divSearch", style={'float':'top','width':'100%','height':'10%','border-style':'solid'}),
html.Div([html.Br(),html.Center('Corpus "Space" de Reddit',style={'font-size':'30px','font-weight':'bold'}),html.Br(),
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
],style_cell={"width":"5px",'minWidth':'5px','maxWidth':'5px'},style_table={'width':'99.5%'}),html.Div(id='divDetailsLeft',children=[html.Div(id='divWordsLeft')],style={'display':'none','float':'left','width':'50%','height':'100%'})],id="divLeft",style={'z-index':'0','float':'left','width':'50%','height':'45%'}),
html.Div([html.Br(),html.Center('Corpus "Space" d\'Arxiv',style={'font-size':'30px','font-weight':'bold'}),html.Br(),
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
],style_cell={"width":"5px",'minWidth':'5px','maxWidth':'5px'},style_table={'width':'99.5%'}),html.Div(id='divDetailsRight',children=[html.Div(id='divWordsRight')],style={'display':'block','float':'right','width':'50%','height':'100%'})],id="divRight",style={'float':'right','width':'50%','height':'90%',"display":"block"})],style={'z-index':'-1'})])
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
     Output("divWordsLeft", "children"),
     Output("divDetailsLeft", "style")],
    Input('tableReddit', 'active_cell'),
    State('tableReddit', 'data'),
    State('txtSearch', 'value'),
)
def callback_func_3(active_cell,data,txt):  
    return_value=()
    if active_cell:
        row = active_cell['row']
        Id=data[row]['Id']  
        #print(Id)
        #print(dfSpaceReddit[dfSpaceReddit['Id'].eq(Id)]['Text'])
        txtDoc = dfReddit[dfReddit['Id'].eq(Id)]['Text']
        if txt:
            score = dfReddit[dfReddit['Id'].eq(Id)]['score'].values[0]
            if score==0.00:
                color = 'rgb(220,220,220)'
            elif score<=0.25:
                color = 'rgb(176,242,182)'
            elif score<=0.5:
                color = 'rgb(104,230,116)'
            else:
                color = 'rgb(47,221,63)' 
                
            dfTFxIdfdup = dfTFxIdf.copy()
            tfxidfWords = []
            keywords_clean = corpus.nettoyer_texte(txt)
            arr_keywords=keywords_clean.split(" ")
            
            tfxidfWords.append(html.B('TfxIdf des mots clés :',style={'font-size':'20px'}))  
            tfxidfWords.append(html.Br()) 
            for word in arr_keywords:
                if word in dfTFxIdf.index:
                    tfxidf = dfTFxIdf.loc[word][dfReddit[dfReddit['Id'].eq(Id)]['Nom']].values[0]
                    if tfxidf==0.0:
                        colorTfxIdf='rgb(220,220,220)'
                    elif tfxidf <=0.25:
                        colorTfxIdf='rgb(176,242,182)'
                    elif tfxidf <=0.5:
                        colorTfxIdf='rgb(104,230,116)'
                    else:
                        colorTfxIdf='rgb(47,221,63)' 
                        
                    value = html.Label(children =[word + ' : ',tfxidf],style={'margin-left':'20px','background-color':colorTfxIdf,'font-size':'20px'})
                else:
                    value = html.Label(children =[word + ' : ',0.0],style={'margin-left':'20px','background-color':'rgb(220,220,220)','font-size':'20px'})
                    
                tfxidfWords.append(value) 
                tfxidfWords.append(html.Br()) 
                
            return_value = html.Div([html.Center([html.Br(),html.B('Score : ',style={'font-size':'25px'}),html.Label(children=[score],style={'background-color':color,'font-size':'20px'}),html.Br(),html.Div(id='divWordsLeft'),html.Br(),html.B('Full text : ',style={'font-size':'25px'}),html.Br(),dcc.Textarea(style={'font-size':'18px'},value=txtDoc,rows=10,cols=30)])]),html.Div(children=tfxidfWords),{'display':'block'}
        else:
            return_value = html.Div([html.Center([html.B('Full text : ',style={'font-weight':'25px'}),html.Br(),html.Div(id='divWordsLeft'),dcc.Textarea(style={'font-size':'18px'},value=dfReddit[dfReddit['Id'].eq(Id)]['Text'],rows=10,cols=30)])]),html.Div(),{'display':'block','border-right':'solid 0.5px'}
    return return_value 

@app.callback(
    [Output("divDetailsRight", "children"),
     Output("divWordsRight", "children"),
     Output("divDetailsRight", "style")],
    Input('tableArxiv', 'active_cell'),
    State('tableArxiv', 'data'),
    State('txtSearch', 'value'),
)
def callback_func_4(active_cell,data,txt):  
    return_value=()
    if active_cell:
        row = active_cell['row']
        Id=data[row]['Id']
        txtDoc = dfArxiv[dfArxiv['Id'].eq(Id)]['Text']
        if txt:
            score = dfArxiv[dfArxiv['Id'].eq(Id)]['score'].values[0]
            if score==0.00:
                color = 'rgb(220,220,220)'
            elif score<=0.25:
                color = 'rgb(176,242,182)'
            elif score<=0.5:
                color = 'rgb(104,230,116)'
            else:
                color = 'rgb(47,221,63)'     
                
            dfTFxIdfdup = dfTFxIdf.copy()
            tfxidfWords = []
            keywords_clean = corpus.nettoyer_texte(txt)
            arr_keywords=keywords_clean.split(" ")
            
            tfxidfWords.append(html.B('tfxidf des mots clés :'))  
            tfxidfWords.append(html.Br()) 
            for word in arr_keywords:
                if word in dfTFxIdf.index:
                    tfxidf = dfTFxIdf.loc[word][dfArxiv[dfArxiv['Id'].eq(Id)]['Nom']].values[0]
                    if tfxidf==0.0:
                        colorTfxIdf='rgb(220,220,220)'
                    elif tfxidf <=0.25:
                        colorTfxIdf='rgb(176,242,182)'
                    elif tfxidf <=0.5:
                        colorTfxIdf='rgb(104,230,116)'
                    else:
                        colorTfxIdf='rgb(47,221,63)' 
                        
                    value = html.Label(children =[word + ' : ',tfxidf],style={'margin-left':'20px','background-color':colorTfxIdf})
                else:
                    value = html.Label(children =[word + ' : ',0.0],style={'margin-left':'20px','background-color':'rgb(220,220,220)'})
                    
                tfxidfWords.append(value) 
                tfxidfWords.append(html.Br()) 
                
            return_value = html.Div([html.Center([html.Br(),html.B('Score : ',style={'font-weight':'15px'}),html.Label(children=[score],style={'background-color':color}),html.Br(),html.Div(id='divWordsRight'),html.Br(),html.B('Full text : '),html.Br(),dcc.Textarea(style={'font-size':'20px'},value=txtDoc,rows=10,cols=30)])]),html.Div(children=tfxidfWords),{'display':'block'}
        else:
            return_value = html.Div([html.Center([html.B('Full text : ',style={'font-weight':'15px'}),html.Br(),html.Div(id='divWordsRight'),dcc.Textarea(style={'font-size':'20px'},value=txtDoc,rows=10,cols=30)])]),html.Div(),{'display':'block','border-left':'solid 0.5px'}
    return return_value 

@app.callback(
   Output(component_id='divInfos', component_property='style'),
   [Input(component_id='dropdown-to-show_or_hide-element', component_property='value')])

def callback_func_5(visibility_state):
    if visibility_state == 'on':
        return {'z-index':'1','display': 'block','width':'100%','height':'100%','position':'absolute','background-color':'white'}
    if visibility_state == 'off':
        return {'z-index':'1','display': 'none','width':'100%','height':'100%','position':'absolute','background-color':'white'}
    
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
