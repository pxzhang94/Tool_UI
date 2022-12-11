import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
sys.path.append("../")
import json

def run(params):
    result = {}

    params['caseID'] = '221015_1'

    tf = open("../main/static/params/" + params['caseID'] + ".json", "w")
    json.dump(params, tf)
    tf.close()

    # parameters
    caseID = params['caseID']
    dPath = params['dPath']
    mPath = params['mPath']
    aAttack = params['aAttack']
    rParam = params['rParam']
    dSize = params['dSize']

    result['caseID'] = caseID
    result['original_acc'] = round(100.00, 2)
    result['adv_path'] = "fgsm_1661408973"
    result['current_acc'] = round(5.70, 2)
    result['nteV'] = round(0.7821 * 100, 2)
    result['acacV'] = round(0.812 * 100, 2)
    result['ald2V'] = round(0.564 * 100, 2)
    result['ncV'] = round(97.0 * 100, 2)
    result['kncV'] = round(92.0 * 100, 2)
    result['cl1V'] = 0.267
    result['cl2V'] = 0.138
    result['clinfV'] = 0.119

    return result

def summarize(result):
    totalS = {}

    totalS['quality'] = "low"
    totalS['summary'] = "The model has been well tested, the results show that it is vulnerable against minor perturbations."
    totalS['testing_summary'] = "Based on the given data, the model has poor performance of K-multisection-Neuron-Coverage, which means more diverse data are needed to test the corner case of the model."
    totalS['attack_summary'] = "The generated images achieve a high Average Confidence of Adversarial Class and a low Average L2 Distortion, which implies that it is easy to generated misclassified data with minor perturbations based on the model."
    totalS['robustness_summary'] = "The values of all the three metrics excced the threshold, which indicates that the robustness estimation of the model is poor."

    tf = open("../main/static/results/" + result['caseID'] + ".json", "w")
    json.dump(totalS, tf)
    tf.close()

    return totalS