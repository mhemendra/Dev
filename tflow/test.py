import numpy as np
import pandas as pd
arr = [i for i in range(1,10)]
pan = pd.DataFrame({'open_price':arr})

num = np.array(pan)
print(pan)
print(num)