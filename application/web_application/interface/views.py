from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

import numpy as np
from tensorflow import keras
from ast import literal_eval

from interface.models import CityData, CategoryData
from interface.serializers import CityDataSerializer, CategoryDataSerializer
from analysis.query import QueryProcess

class CityDataViewSet(viewsets.ModelViewSet):
    queryset = CityData.objects.all()
    serializer_class = CityDataSerializer
    permission_classes = [AllowAny]

    '''
    @action(methods=['GET'], detail=False)
    def insertion(self, request):
        query_process = QueryProcess()
        for t in query_process.city_name().values:
            q = CityData(city=t[0])
            q.save()
    '''
    @action(methods=['GET'], detail=False)
    #def prediction(self, request, city, category, year, month, day):
    def prediction(self, request):
        city = request.query_params["city"]
        category = request.query_params["category"]
        year = request.query_params["year"]
        month = request.query_params["month"]
        day = request.query_params["day"]

        query_process = QueryProcess()
        data = query_process.query_dataset(year, city, category)

        # As only has data at most 2018-12-31, test for 2018-12-31
        test_data = data.tail(32)
        test_data = np.array([test_data.values[:, :15]])

        new_model = keras.models.load_model('./interface/model_{0}_{1}.h5'.format(city, category))
        normalize_info = np.genfromtxt("./interface/{0}_{1}_normalize.csv".format(city, category), delimiter=",")

        return Response((new_model.predict(test_data)*normalize_info[1] + normalize_info[0]).astype(int))

    @action(methods=['GET'], detail=False)
    def posterior_analysis(self, request):
        city = request.query_params["city"]
        category = request.query_params["category"]

        f = open("../results/feature_selection/{0}_{1}.txt".format(city, category))
        result = [str(r).rstrip("\n") for r in f.readlines()]
        
        return Response(result)
        

class CategoryDataViewSet(viewsets.ModelViewSet):
    queryset = CategoryData.objects.all()
    serializer_class = CategoryDataSerializer
    permission_classes = [AllowAny]

    @action(methods=['GET'], detail=False)
    def insertion(self, request):
        table_name = request.query_params["table"]
        data = literal_eval(request.query_params["data"])

        return Response(data)