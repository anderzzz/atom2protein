from server.presenter_webapp.models import PresenterDataViz
from server.presenter_webapp.serializers import PresenterDataVizSerializer
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

from server.presenter_webapp.serializers import SearchStructureSerializer, \
                                                SummaryPropertySerializer, \
                                                PresentationVizSerializer
from server.presenter_webapp.forms import SearchStructureForm, \
                                          SummaryPropertyForm, \
                                          PresentationVizForm
from server.presenter_webapp.models import RetrieverStructure 

from informatics.launchers import Launcher

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

class SourcePosts(View):
    def get(self, request, pk, format=None):
        postables = []
        presenter_model_instances = PresenterDataViz.objects.filter(data_source__id=pk)
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

def search_n_launch(request):
    '''View to get the search and calculation launch page, as well as post the
    command to execute by the search and presentation algorithms.

    Parameters
    ----------
    request, object
        The HTTP request object obtained from the URL.

    '''
    if request.method == 'GET':
        form_search = SearchStructureForm()
        form_summary = SummaryPropertyForm()
        form_pres = PresentationVizForm()

    else:
         
        form_search = SearchStructureForm(request.POST)
        form_summary = SummaryPropertyForm(request.POST)
        form_pres = PresentationVizForm(request.POST)
        posted_forms = {'search' : form_search,
                        'summary' : form_summary,
                        'pres' : form_pres}

        valid_check = all([form.is_valid() for form in list(posted_forms.values())])

        if valid_check:
            # Retrieve posted input and format as needed to create model object
            posted_input = dict([(key, form.cleaned_data) for key, form in
                                                          posted_forms.items()])
            total_input = posted_input['search'].copy()
            for key, post_inp in posted_input.items():
                total_input.update(post_inp)

            retriever_cmd = RetrieverStructure.objects.create(**total_input)
            retriever_cmd.save()

            # The launcher to the computation algorithm requires JSON input
            serial_search = SearchStructureSerializer(retriever_cmd).data
            serial_summary = SummaryPropertySerializer(retriever_cmd).data
            serial_pres = PresentationVizSerializer(retriever_cmd).data
            serial_input = {'rawdata_type' : 'protein_structure',
                            'search_instructions' : serial_search,
                            'summary_instructions' : serial_summary,
                            'presentation_instructions' : serial_pres}
            json_data = JSONRenderer().render(serial_input).decode("utf-8")
            print (json_data)

            # Launch calculation
            statement_creator = Launcher(json_data)
            statement_creator.launch()

            return HttpResponseRedirect('/sourceposts/' + str(retriever_cmd.id))

    return render(request, 'retriever/retrieve_main.html', 
                           {'form_search': form_search, 
                            'form_summary': form_summary,
                            'form_pres': form_pres})
