# blockchain.py

from blockchainCardano import blockchainCardano as car
from myapp_forms import LoginForm

balance_bp = Blueprint('balance', __name__)

@balance_bp.route('/balance', methods=['GET', 'POST'])
def balance(address):
    form = LoginForm()
    
    if request.method == 'POST':
        address = request.form['address']
        balance = car.get_balance(address)
        json_balance = jsonify({"balance": balance})
        return render_template('cardano.html', json=json_balance)
    else:
        json_balance = ''
        return render_template('cardano.html', json=json_balance)
