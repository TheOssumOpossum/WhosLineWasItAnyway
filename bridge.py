from flask import Flask
from Read_data import test2
#from preprocessing import PreProcessing
#from Transcript import Program


app = Flask(__name__)

@app.route("/")
def test():
    return test2()

if __name__ == "__main__":
    app.run()
