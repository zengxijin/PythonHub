import h2o
h2o.init()

model = h2o.load_model("GBM_ForLoanPredict.zip")
h2o.download_pojo(model, path='./', get_jar=True)
