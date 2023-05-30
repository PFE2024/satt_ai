
RUN pip install -r requirements2_venv.txt
RUN python3 -m spacy download en_core_web_sm
RUN python3 -c "import nltk; nltk.download('punkt')"
RUN python3 -c "import nltk; nltk.download('averaged_perceptron_tagger')"
python3 -m nltk.downloader stopwords


create envirenment:
python3.8 -m venv env

activate env :
in windows:
venv/Scripts/Activate.ps1


 in Mac:
source venv/bin/activate
desactivate env:
deactivate



create requirements.txt:
pip freeze > requirements2_venv.txt

install requirements.txt:
pip install -r requirements2_venv.txt

detecter les package  utiliser dans le code:
pipreqs --savepath requirements.txt