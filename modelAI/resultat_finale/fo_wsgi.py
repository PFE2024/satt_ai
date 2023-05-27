from waitress import serve
from fo_app import app1

if __name__ == "__main__":
  
    serve(app1, host="0.0.0.0", port=8081)