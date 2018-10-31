"""
  author zengxijin created on 2018/10/31
"""
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

work_dir = "D:/github/PythonHub/h2o-work"
mojo_file_path = work_dir + "/GBM_ForLoanPredict.zip"
h2o_jar_path = work_dir + "/venv/Lib/site-packages/h2o/backend/bin/h2o.jar"
gv_file_path = work_dir + "/GBM_ForLoanPredict.gv"
image_file_path = work_dir + "/GBM_ForLoanPredict.png"
win_install_graphviz_path = "C:\\Program Files (x86)\\Graphviz2.38\\bin\\"

# 保存模型
model.download_mojo(mojo_file_path)


def generateTree2Gv(h2o_jar_path, mojo_file_path, gv_file_path, tree_id=0):
    result = subprocess.call(
        ["java", "-cp", h2o_jar_path, "hex.genmodel.tools.PrintMojo", "--tree", str(tree_id), "-i", mojo_file_path,
         "-o", gv_file_path], shell=False)
    print("Graphviz file " + gv_file_path + " is generated.")


def generateTreeImage(gv_file_path, image_file_path):
    result = subprocess.call([win_install_graphviz_path + "dot", "-Tpng", gv_file_path, "-o", image_file_path], shell=True)


generateTree2Gv(h2o_jar_path, mojo_file_path, gv_file_path, 0)
generateTreeImage(gv_file_path, image_file_path)

# 或者cd到目录C:\Program Files (x86)\Graphviz2.38\bin，执行以下命令，生成决策树的图
# dot -Tpng D:/github/PythonHub/h2o-work/GBM_ForLoanPredict.gv -o D:/github/PythonHub/h2o-work/GBM_ForLoanPredict.png
