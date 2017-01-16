from server.presenter_webapp.models import PresenterDataViz
from server.presenter_webapp.serializers import PresenterDataVizSerializer
from server.presenter_webapp.serializers import RetrieverStructureSerializer
from django.http import Http404
from django.template import loader
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from .forms import RetrieverForm 
from server.presenter_webapp.models import RetrieverStructure 
import sys
sys.path.append('/home/anderzzz/ideas/protein')
from statement_creator import Launcher

class PresenterDataVizList(APIView):
    '''List all protein data visualization, or create new one

    '''
    def get(self, request, format=None):
        '''GET method'''
        viz = PresenterDataViz.objects.all()
        serializer = PresenterDataVizSerializer(viz, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        '''POST method'''
        serializer = PresenterDataVizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class RetrieverStructureView(APIView):


class PresenterDataVizDetail(APIView):
    '''Retrieve, update or delete visualization instance

    '''
    def get_object(self, pk):
        try:
            return PresenterDataViz.objects.get(pk=pk)
        except PresenterDataViz.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''GET method'''
        viz = self.get_object(pk)
        serializer = PresenterDataVizSerializer(viz)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        '''PUT method'''
        viz = self.get_object(pk)
        serializer = PresenterDataVizSerializer(viz)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        '''DELETE method'''
        viz = self.get_object(pk)
        viz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PresenterViz(APIView):
    '''Retrieve visualization file at given path

    '''
    def get_object(self, pk):
        try:
            return PresenterDataViz.objects.get(pk=pk)
        except PresenterDataViz.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''GET method'''
        viz = self.get_object(pk)
        serializer = PresenterDataVizSerializer(viz)
        file_dir = serializer.data['viz_file_path']
        with open(settings.BASE_DIR + file_dir) as fin:
            content = fin.read()
        template = loader.get_template('presenter_vizscroll/statement.html')
        context = {'content' : content}
        return Response(template.render(context, request))

class ViewViz(View):
    '''Simple view of HTML visualization

    '''
    def get_object(self, pk):
        try:
            return PresenterDataViz.objects.get(pk=pk)
        except PresenterDataViz.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''GET method'''
        viz = self.get_object(pk)
        serializer = PresenterDataVizSerializer(viz)
        file_dir = serializer.data['viz_file_path']
        with open(settings.BASE_DIR + file_dir) as fin:
            content = fin.read()
        template = loader.get_template('presenter_vizscroll/statement.html')
        context = {'content' : content}
        return HttpResponse(template.render(context, request)) 

class AllPosts(View):
    '''Super simple stuff

    '''
    def get(self, request, format=None):
        '''GET method'''
        postables = []

        presenter_model_instances = PresenterDataViz.objects.all()
        for model in presenter_model_instances:
            d_out = {}

            data_file_root = model.file_path + '/' + model.file_namespace
            with open(data_file_root + '.html_div') as fin:
                d_out['div'] = fin.read()
            with open(data_file_root + '.js') as fin:
                d_out['script'] = fin.read()

            d_out['created_time'] = str(model.created_time)
            d_out['entry_data_text'] = model.entry_data_type

            postables.append(d_out)

        template = loader.get_template('presenter_vizscroll/list_of_viz.html')
        context = {'posts' : postables}
        return HttpResponse(template.render(context, request)) 

def post_simple(request):
    if request.method == 'GET':
        form = RetrieverForm()
    else:
        form = RetrieverForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            resolution = form.cleaned_data['resolution_min']
            retriever_cmd = RetrieverStructure.objects.create(title=title,
                                                 resolution_min=resolution,
                                                 resolution_max=resolution)
            retriever_cmd.save()
            serializer = RetrieverStructureSerializer(retriever_cmd)
            print (serializer.data)
            json_data = JSONRenderer().render(serializer.data).decode("utf-8")
            print (json_data)
            statement_creator = Launcher(json_data)
            # My thinking is to serialize model, send to a "statement creator"
            # which parses the JSON and launches a calculation, returns the new
            # visualization entry ID for loading.
            xx=proteinmeta.launcher(serializer.data)
            return HttpResponseRedirect('/retriever')

    return render(request, 'retriever/simple.html', {'form': form})
