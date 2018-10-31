import h2o
import subprocess
from h2o.estimators.gbm import H2OGradientBoostingEstimator

# (0)初始化
h2o.init()

# (1)加载数据
data = "./data/loan.csv"
loans = h2o.import_file(path=data)
loans["bad_loan"] = loans["bad_loan"].asfactor()
print("total records: %s" % len(loans))

Y = "bad_loan"
X = ["loan_amnt", "longest_credit_length", "revol_util", "emp_length",
     "home_ownership", "annual_inc", "purpose", "addr_state", "dti",
     "delinq_2yrs", "total_acc", "verification_status", "term"]

# (2)训练和验证数据拆分，80%训练，20%验证
rand = loans.runif(seed=10086)  # 添加一列数据[0,1)之间，(使用h2o.spiltFrame()这种方式也可以拆分)
train = loans[rand <= 0.8]
valid = loans[rand > 0.8]
print("train data records: %s (%s)" % (len(train), len(train) / len(loans)))
print("valid data records: %s (%s)" % (len(valid), len(valid) / len(loans)))

# use GBM algorithm, and set the hyperparameters(超参)
model = H2OGradientBoostingEstimator(score_each_iteration=True,
                                     ntrees=100,
                                     max_depth=5,
                                     learn_rate=0.05,
                                     model_id="GBMForLoanPredict")
# (3)train and predict
model.train(x=X, y=Y, training_frame=train, validation_frame=valid)
print(model)

# Getting all cross validated models
# all_models = model.cross_validation_models()  # nfolds才有
# print("Total cross validation models: %s" % len(all_models))


mojo_file_name = "D:/github/PythonHub/h2o-work/GBM_ForLoanPredict.zip"
h2o_jar_path = 'D:/github/PythonHub/h2o-work/venv/Lib/site-packages/h2o/backend/bin/h2o.jar'
mojo_full_path = mojo_file_name
gv_file_path = "D:/github/PythonHub/h2o-work/GBM_ForLoanPredict.gv"
image_file_name = "D:/github/PythonHub/h2o-work/GBM_ForLoanPredict.png"

model.download_mojo(mojo_file_name)

def generateTree(h2o_jar_path, mojo_full_path, gv_file_path, image_file_path, tree_id=0):
    result = subprocess.call(
        ["java", "-cp", h2o_jar_path, "hex.genmodel.tools.PrintMojo", "--tree", str(tree_id), "-i", mojo_full_path,
         "-o", gv_file_path], shell=False)
    print("Graphviz file " + gv_file_path + " is generated.")
    # result = subprocess.call(["ls", gv_file_path], shell=False)  # can't run in windows
    # if result is 0:
    #     print("Success: Graphviz file " + gv_file_path + " is generated.")
    # else:
    #     print("Error: Graphviz file " + gv_file_path + " could not be generated.")

win_graphviz_path = "C:/Program Files (x86)/Graphviz2.38/bin"


def generateTreeImage(gv_file_path, image_file_path, tree_id):
    image_file_path = image_file_path + "_" + str(tree_id) + ".png"

    import sys
    sys.path.append(win_graphviz_path)
    result = subprocess.call(["dot", "-Tpng", gv_file_path, "-o", image_file_path], shell=False)

    # result = subprocess.call(["ls", image_file_path], shell=False)
    # if result is 0:
    #     print("Success: Image File " + image_file_path + " is generated.")
    #     print("Now you can execute the follow line as-it-is to see the tree graph:")
    #     print("Image(filename='" + image_file_path + "\')")
    # else:
    #     print("Error: Image file " + image_file_path + " could not be generated.")


# Just change the tree id in the function below to get which particular tree you want
generateTree(h2o_jar_path, mojo_full_path, gv_file_path, image_file_name, 0)
# Note: If this step hangs, you can look at "dot" active process in osx and try killing it
generateTreeImage(gv_file_path, image_file_name, 3)
# g = Graph(format='gv', filename=gv_file_path)
# g.render(format='png', filename=image_file_name, view=False)
