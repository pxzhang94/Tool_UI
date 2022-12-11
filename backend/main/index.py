import os
import sys
current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)
sys.path.append("../../TEA/")

# STATIC_URL = '/static/'
# STATICFILES_DIRS=[
#     os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'static')
# ]

from backend.tutorial import run, summarize
from aid_data.load_data import load_adv_file
from aid_util.configs import dConfig

import json
import pickle
from bs4 import BeautifulSoup
import util
import time

print('begin')

from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/result/<params>')
def get_result(params):
	params_dict = json.loads(params.replace("'",'"'))

	# attack method
	if params_dict['aAttack'] == 'None':
		if params_dict['rNoise'] == 'None':
			params_dict['aAttack'] = 'FGSM'
		else:
			params_dict['aAttack'] = params_dict['rNoise']

	# data size
	params_dict['dSize'] = float(params_dict['dSize'].split("%")[0]) / 100.0
	result = run(params_dict)
	print(result['lcV'])

	summary = summarize(result)

	adv_files = load_adv_file(result['adv_path'])

	return render_template('result.html', params = params_dict, result = result, summary=summary, adv_files = adv_files, data_name = dConfig.dName)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/result/<params>', methods = ['POST','GET'])
def diagnose2():
	if request.method == 'POST':
		params = request.form.to_dict() # {'mPath': 'MOM EP and S Pass Application Form_ZhangPeixin.pdf', 'rNoise': 'Gaussian noise', 'nDegree': '0.1', 'dPath': 'Application Form (Admin & Research positions)_ZhangPeixin.pdf', 'aAttack': 'JSMA', 'dSize': '10%'}
		print(params)
		if params:
			return redirect(url_for('get_result', params=params))
		else:
			return redirect(url_for('index'))

@app.route('/index', methods = ['POST','GET'])
def diagnose1():
	if request.method == 'POST':
		params = request.form.to_dict() # {'mPath': 'MOM EP and S Pass Application Form_ZhangPeixin.pdf', 'rNoise': 'Gaussian noise', 'nDegree': '0.1', 'dPath': 'Application Form (Admin & Research positions)_ZhangPeixin.pdf', 'aAttack': 'JSMA', 'dSize': '10%'}
		if params:
			if 'mPath' not in params.keys():
				model_files = request.files['mPath']
				if model_files.filename != '':
					model_files.save(os.path.join('static/models/', model_files.filename))
					params['mPath'] = model_files.filename
			if 'dPath' not in params.keys():
				data_files = request.files['dPath']
				if data_files.filename != '':
					data_files.save(os.path.join('static/datasets/', data_files.filename))
					params['dPath'] = data_files.filename
			return redirect(url_for('get_result', params=params))
		else:
			return redirect(url_for('index'))

		# qestion_query = request.form['query'].replace("/","")
		# if qestion_query:
		# 	return redirect(url_for('get_result',query_x = qestion_query))
		# else:
		# 	return redirect(url_for('index'))
	# if request.method == 'GET':
	# 	qestion_query = request.args.get['query'].replace("/","")
	# 	if qestion_query:
	# 		return redirect(url_for('get_result',query_x = qestion_query))
	# 	else:
	# 		return redirect(url_for('index'))

if __name__ == '__main__':
    # app.run(host='0.0.0.0',port='58888')
    app.run(host='0.0.0.0', port='2267', debug=True)
    # app.run(debug=True)
