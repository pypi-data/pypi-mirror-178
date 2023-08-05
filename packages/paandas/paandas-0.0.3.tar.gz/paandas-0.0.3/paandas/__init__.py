def multiplicative_congruential_method():
    return '''
    def multiplicative_congruential_method(a, m, l):
        result = [1]

        # generate random number
        for i in range(l-1):
            result.append((a*result[-1])%m)

        # show graph of the generated random number
        plt.hist(result, bins=15)
        plt.show()
        
        return

    multiplicative_congruential_method(7, 233, 10000)'''

def generateSumArray():
    return'''
    def generateSumArray(length, max):
        result = []
        for i in range(length):
            temp = []
            sum = 0
            while sum < max:
            randNum = random.uniform(0,1)
            temp.append(randNum)
            sum += randNum
            result.append(len(temp))
        return result

    a = np.mean(generateSumArray(100, 1))
    print("a ->", a)

    b = np.mean(generateSumArray(1000, 1))
    print("b ->", b)

    c = np.mean(generateSumArray(10000 , 1))
    print("c ->", c)

    print("observation ->", "value of E(N) is almost equal", a, "~", b, "~", c)'''

def generateProbArray():
    return'''
    def generateProbArray(length, max):
        result = []
        for i in range(length):
            temp = []
            prod = 1
            while prod > max:
            randNum = random.uniform(0,1)
            temp.append(randNum)
            prod *= randNum
            temp.pop()
            result.append(len(temp))
        return result

    arr = generateProbArray(10, np.exp(-3))
    a = np.mean(arr)
    print("a ->", a)
    print("arr ->", arr)

    for i in range(7):
    print("P[N="+str(i)+"] ->", len(np.where(np.array(arr) == i)[0])/len(arr))
'''

def plot_hist_and_den():
    return '''
    # plot histogram and density for given feature
    def plot_hist_and_den(df, feature, bins):
        arr = df[feature]
        sns.distplot(arr, color="r", bins=bins)
        plt.show()
    
    features = list(df.columns)
    for i in features:
        plot_hist_and_den(df, i, 20)'''

def scatter_plot_2D_Grid():
    return '''
    # plot 2D scatter graph for all feature
    def scatter_plot_2D(df):
        grid2D = sns.PairGrid(df)
        grid2D.map(sns.scatterplot)
    
    scatter_plot_2D(df)'''

def scatter_plot_3D():
    return '''
    def scatter_plot_3D(df, feature1, feature2, feature3):
        plt.figure(figsize = (10, 10))
        axes = plt.axes(projection ="3d")
        axes.scatter3D(df[feature1], df[feature2], df[feature3])
        axes.set_xlabel(feature1)
        axes.set_ylabel(feature2)
        axes.set_zlabel(feature3)
    
    features = list(df.columns)
    scatter_plot_3D(df, features[0], features[1], features[2])'''

def find_standard_deviation():
    return '''
    # find standard deviation of given feature
    def find_standard_deviation(df, feature):
        mean_value = df[feature].mean()
        result = 0
        for i in range(len(df)):
            result += (df[feature][i]-mean_value)**2
        return (result/(len(df)-1))**(1/2)
    
    standard_deviation_arr = []
    features = list(df.columns)
    for i in features:
        standard_deviation_arr.append(find_standard_deviation(df, i))
    print("standard deviation ->", standard_deviation_arr)'''

def find_variance():
    return '''
    # find variance of given feature
    def find_variance(df, feature):
        mean_value = df[feature].mean()
        result = 0
        for i in range(len(df)):
            result += (df[feature][i]-mean_value)**2
        return (result/(len(df)-1)) 
    
    features = list(df.columns)
    variance_arr = []
    for i in features:
        variance_arr.append(find_variance(df, i))
    print("variance ->", variance_arr)'''

def find_correlation():
    return '''
    # find correlation
    def find_correlation(df, feature1, feature2):
        mean_feature1 = df[feature1].mean()
        mean_feature2 = df[feature2].mean()
        result = 0
        for i in range(len(df)):
            result += (df[feature1][i]-mean_feature1) * (df[feature2][i]-mean_feature2)
        cov = result/(len(df)-1)
        sd_feature1 = find_standard_deviation(df,feature1)
        sd_feature2 = find_standard_deviation(df, feature2)
        return (cov)/(sd_feature1 * sd_feature2)
    
    from itertools import combinations
    all_pair = list(combinations(features, 2))
    for i in all_pair:
        cor= find_correlation(df, i[0], i[1])
        print("correlation",i[0],"+",i[1],"->",cor)'''

def find_standardization():
    return '''
    # find standardization
    def find_standardization(df, feature):
        arr = []
        for i in range(len(df)):
            mean_value = df[feature].mean()
            sd_feature = find_standard_deviation(df, feature)
            arr.append((df[feature][i]-mean_value)/sd_feature) 
        return arr
    
    standardization_arr = []
    features = list(df.columns)
    for i in features:
        standardization_arr = find_standardization(df, i)
    print("standardization ->", standardization_arr)'''

def find_normalization():
    return '''
    # find normalization
    def find_normalization(df, feature):
        arr = []
        for i in range(len(df)):
            arr.append((df[feature][i]-find_min(df, feature))/(find_max(df, feature)-find_min(df, feature))) 
        return arr
    
    normalization_arr = []
    features = list(df.columns)
    for i in features:
        normalization_arr = find_normalization(df, i)
    print("normalization ->", normalization_arr)'''

def gdumc():
    return '''
    # generate equiprobable class
    def generate_class(mean, cov, n):
        return np.random.multivariate_normal(mean, cov, n)

    # plot 3D scatter graph
    def scatter_plot_3D(dataset):
        plt.figure(figsize = (10, 10))
        axes = plt.axes(projection ="3d")
        axes.scatter3D(dataset.T[0], dataset.T[1], dataset.T[2], color="r")
        plt.show()
    
    class1 = generate_class([1, 1], [[1, 0], [0, 1]], 333)
    class2 = generate_class([7, 7], [[1, 0], [0, 1]], 333)
    class3 = generate_class([15, 1], [[1, 0], [0, 1]], 334)
    dataset = np.append(np.append(class1, class2, axis=0), class3, axis=0)
    sns.scatterplot(dataset.T[0], dataset.T[1], color="r")
    plt.show()
    
    class1 = generate_class([1, 1, 1], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], 333)
    class2 = generate_class([7, 7, 7], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], 333)
    class3 = generate_class([15, 1, 7], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], 334)
    dataset = np.append(np.append(class1, class2, axis=0), class3, axis=0)
    scatter_plot_3D(dataset)'''

def Decision_Tree():
    return '''
    import numpy as np
    import pandas as pd
    from sklearn import tree
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score
    from sklearn.ensemble import RandomForestClassifier
    import matplotlib.pyplot as plt
    
    def create_decision_tree(dataset, target_col):
        data = dataset.drop([target_col], axis=1)
        targets = dataset[target_col]
        x_train, x_test, y_train, y_test = train_test_split(data, targets, test_size=0.2, random_state=30)
        model = DecisionTreeClassifier()
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        return [model, accuracy_score(y_test, predictions)]

    def create_pruned_decision_tree(dataset, target_col, height):
        data = dataset.drop([target_col], axis=1)
        targets = dataset[target_col]
        x_train, x_test, y_train, y_test = train_test_split(data, targets, test_size=0.2, random_state=30)
        model = DecisionTreeClassifier(max_depth=height)
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        return [model, accuracy_score(y_test, predictions)]
    
    banknote, accuracy = create_decision_tree(df_banknote, 'class')
    print("banknote accuracy:", accuracy)
    
    fig = plt.figure(figsize=(25,20))
    figure = tree.plot_tree(banknote, feature_names=df_banknote.columns, class_names='class', filled=True)'''

def kmeans():
    return '''
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    def generate_class(mean, cov, n):
        return np.random.multivariate_normal(mean, cov, int(n))
    
    def kmean(cluster, dataset):
        seed = dataset[np.random.choice(dataset.shape[0], cluster, replace=False)]
        while True:
            result = [[] for i in range(cluster)]
            for i in range(len(dataset)):
                dist = np.linalg.norm(seed - dataset[i], axis=1)
                index = np.where(dist == np.amin(dist))[0][0]
                result[index].append(dataset[i])
            temp = list(map(lambda x:np.mean(x, axis=0), result))
            if np.array_equal(seed, temp):
                return result
            else:
                seed = temp
        return np.array(result)
    
    def find_mean(arr):
        result = []
        for elm in arr:
            result.append(np.mean(elm, axis=0))
        return np.array(result)
    def find_correct_count(result, dataset):
        count = 0
        for elm in result:
            if elm in dataset:
            count += 1
        return count
    def accuracy(result, dataset, ln):
        upd_result = find_mean(result)
        upd_dataset = find_mean(dataset)
        f_count = 0
        for i in range(len(upd_dataset)):
            dist = np.linalg.norm(upd_result - upd_dataset[i], axis=1)
            index = np.where(dist == np.amin(dist))[0][0]
            f_count += find_correct_count(result[index], dataset[i])
        return f_count/ln
    
    def print_scatter_plot(arr, title):
        for i in range(len(arr)):
            plt.scatter(np.array(arr[i]).T[0], np.array(arr[i]).T[1])
        plt.title(title)
        plt.show()
    
    mean = np.random.default_rng().integers(low=0, high=100, size=2)
    temp = np.random.randint(-100,100,size=(2,2))
    cov = (temp + temp.T)/2
    clt1 = generate_class(mean, cov, 50)
    mean = np.random.default_rng().integers(low=0, high=100, size=2)
    temp = np.random.randint(-100,100,size=(2,2))
    cov = (temp + temp.T)/2
    clt2 = generate_class(mean, cov, 50)
    mean = np.random.default_rng().integers(low=0, high=100, size=2)
    temp = np.random.randint(-100,100,size=(2,2))
    cov = (temp + temp.T)/2
    clt3 = generate_class(mean, cov, 50)
    dataset1 = np.concatenate((clt1, clt2, clt3), axis=0)
    
    for i in range(5):
        result = kmean(3, dataset1)
        print("Accuracy:", accuracy(result, [clt1, clt2, clt3], 150))
        print_scatter_plot(result, "Predicted Clusters")
        print("----------------------------------------------------")'''

def gambling():
    return '''
    import random
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    def gambling_model(prob, n, i):
        choices = np.arange(n + 1)
        positions = [i]
        while(i < n and i > 0):
            move = np.random.choice([1, -1], 1, p=[prob, 1 - prob])[0]
            i = i + move
            positions.append(i)
        return choices, positions
    
    c, p = gambling_model(0.5, 10, 4)
    print(p)
    
    sns.lineplot(data=p)'''

def bayesian_model():
    return '''
    !pip install pgmpy
    
    from pgmpy.models import BayesianModel
    from pgmpy.factors.discrete import TabularCPD
    from pgmpy.inference import VariableElimination
    
    model = BayesianModel([('D', 'G'), ('I', 'G'), ('G', 'L'), ('I', 'S')])
    
    cpd_d = TabularCPD(variable='D', variable_card=2, values=[[0.6], [0.4]])
    cpd_i = TabularCPD(variable='I', variable_card=2, values=[[0.7], [0.3]])
    cpd_g = TabularCPD(variable='G', variable_card=3,
                    values=[[0.3, 0.05, 0.9,  0.5],
                            [0.4, 0.25, 0.08, 0.3],
                            [0.3, 0.7,  0.02, 0.2]],
                    evidence=['I', 'D'],
                    evidence_card=[2, 2])

    cpd_l = TabularCPD(variable='L', variable_card=2,
                    values=[[0.1, 0.4, 0.99],
                            [0.9, 0.6, 0.01]],
                    evidence=['G'],
                    evidence_card=[3])

    cpd_s = TabularCPD(variable='S', variable_card=2,
                    values=[[0.95, 0.2],
                            [0.05, 0.8]],
                    evidence=['I'],
                    evidence_card=[2])
    
    model.add_cpds(cpd_d, cpd_i, cpd_g, cpd_l, cpd_s)
    model.check_model()
    
    print(cpd_d)
    print(cpd_i)
    print(cpd_g)
    print(cpd_s)
    print(cpd_l)
    
    infer = VariableElimination(model)
    
    print(infer.query(['G'], evidence={'D': 0, 'I': 1}))
    
    print(infer.query(['L'], evidence={'I': 1}))'''

def help():
    return '''
    Original Name: Function Name
    Multiplicative Congruential Method: multiplicative_congruential_method()
    Generate Sum Array: generateSumArray()
    Generate Product Array: generateProbArray()
    Histogram with Density: plot_hist_and_den()
    Scatter Plot with Grid: scatter_plot_2D_Grid()
    Scatter plot 3D: scatter_plot_3D()
    Standard Deviation: find_standard_deviation()
    Varience: find_variance()
    Correlation of pair of 2 features: find_correlation()
    Standardization: find_standardization()
    Normalization: find_normalization()
    Generate Dataset using mean and covarience: gdumc()
    Decision Tree and Random Forest: Decision_Tree()
    Gambling: gambling()
    Bayesian Model: bayesian_model()
    K-Means: kmeans()'''