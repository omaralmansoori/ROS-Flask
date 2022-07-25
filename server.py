from flask import Flask, send_file
from flask_restx import Api, Resource
from csv import reader
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime

plt.style.use('_mpl-gallery')
matplotlib.use('Agg')

app = Flask(__name__)
api = Api(app, title='AV Lab Project', description='')


@api.route('/<robot>/<x>/<y>')
class Update(Resource):
    def post(self, robot, x, y):
        file = open(f'{robot}_loc.csv', 'a')
        date = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
        file.writelines([f"{date}, {x}, {y}\n"])
        file.close()
        return 200

@api.route('/<robot>')
class Read(Resource):
    def get(self, robot):
        with open(f'{robot}_loc.csv', 'r') as f:
            last_line = f.readlines()[-1]
            params = last_line.split(',')
            x = float(params[1])
            y = float(params[2])
            self.plot(x, y)
            plt.savefig(f'{robot}.png')
        return send_file(f'{robot}.png', mimetype='image/png')
    
    def plot(self, x, y):
        plt.style.use('_mpl-gallery')
        fig, ax = plt.subplots()
        ax.scatter(x, y, s=[50], c=[50], vmin=0, vmax=15)
        ax.set(xlim=(0, 15), xticks=[i for i in range(0, 15)],
                ylim=(0, 15), yticks=[i for i in range(0, 15)])



if __name__ == "__main__":
    app.run()