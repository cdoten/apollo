# Create your views here.
from django.http import HttpResponse
from webapp.models import *
from models import *
from api import *
from queries import checklist_status
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from djangomako.shortcuts import render_to_string
import json
from xlwt import *
from datetime import datetime
from stats import *
from django.views.decorators.cache import cache_page
from stream_status_queries import *

@cache_page(5)
@login_required
def dashboard_stats(request):
    province = request.GET.get('province', None)
    district = request.GET.get('district', None)
    polling_district = request.GET.get('polling_district', None)
    polling_stream = request.GET.get('polling_stream', None)
    sample = request.GET.get('sample', None)
    
    # checklist statistics
    checklist_filter = {}
    
    if polling_stream:
        try:
            checklist_filter['location__id'] = int(polling_stream)
        except ValueError:
            pass
    elif polling_district:
        try:
            checklist_filter['location__parent__parent__id'] = int(polling_district)
        except ValueError:
            pass
    elif district:
        try:
            checklist_filter['location__parent__parent__parent__parent__parent__id'] = int(district)
        except ValueError:
            pass
    elif province:
        try:
            checklist_filter['location__parent__parent__parent__parent__parent__parent__id'] = int(province)
        except ValueError:
            pass
    if sample:
        checklist_filter['location__pk__in'] = Sample.objects.filter(sample=sample).values_list('location__pk', flat=True)
    
    dashboard_checklist_status = {
        'setup_complete': Checklist.objects.filter(**checklist_filter).filter(**checklist_status['setup_complete']).count(),
        'setup_missing': Checklist.objects.filter(**checklist_filter).filter(**checklist_status['setup_missing']).count(),
        'setup_partial': Checklist.objects.filter(**checklist_filter).filter(checklist_status['setup_partial']).count(),
        
        'voting_complete': Checklist.objects.filter(**checklist_filter).filter(**checklist_status['voting_complete']).count(),
        'voting_missing': Checklist.objects.filter(**checklist_filter).filter(**checklist_status['voting_missing']).count(),
        'voting_partial': Checklist.objects.filter(**checklist_filter).filter(checklist_status['voting_partial']).count(),
        
        'closing_complete': Checklist.objects.filter(**checklist_filter).filter(**checklist_status['closing_complete']).count(),
        'closing_missing': Checklist.objects.filter(**checklist_filter).filter(**checklist_status['closing_missing']).count(),
        'closing_partial': Checklist.objects.filter(**checklist_filter).filter(checklist_status['closing_partial']).count(),
        
        'counting_complete': Checklist.objects.filter(**checklist_filter).filter(**checklist_status['counting_complete']).count(),
        'counting_missing': Checklist.objects.filter(**checklist_filter).filter(**checklist_status['counting_missing']).count(),
        'counting_partial': Checklist.objects.filter(**checklist_filter).filter(checklist_status['counting_partial']).count(),
    }
         
    return HttpResponse(json.dumps(dashboard_checklist_status), mimetype="application/json")

@login_required
@permission_required('webapp.can_export')
def export_checklists(request):
    request_params = request.GET
    resource = ChecklistsResource()
    
    applicable_filters = resource.build_filters(request_params)
    obj_list = list(resource.apply_filters(request, applicable_filters))
    
    wb = Workbook()
    ws = wb.add_sheet('Checklists');
    
    if settings.ZAMBIA_DEPLOYMENT == 'RRP':
        # write row header
        columns = ['PDID', 'Monitor Id', 'Monitor Name', 'Monitor Phone', 'Supervisor Name', 'Supervisor Phone', 'Time', 'Province', 'District', 'Constituency', 'Ward', 
            'Polling District', 'Polling Station', 'Polling Stream',
            '1', '2', '3a', '3b', '3c', '3d', '3e', '3f', '3g', '3h', '4', '5', '5a',
            '5b', '5c', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
            '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', 
            '28a1', '28a2', '28b1', '28b2', '28c1', '28c2', '28d1', '28d2', '28e1', '28e2',
            '29a1', '29b1', '29c1', '29d1', '29e1', '29f1', '29g1', '29h1', '29i1', '29j1', '29k1', '29l1', 
            '29a2', '29b2', '29c2', '29d2', '29e2', '29f2', '29g2', '29h2', '29i2', '29j2', '29k2', '29l2',  
            '30', '31', '32', '33']
    
        data_fields = ['location.parent.code', 'observer.observer_id', 'observer.name', 'observer.connection_set.all()[0].identity', 'observer.supervisor.name', 'observer.supervisor.connection_set.all()[0].identity', 
            'response.updated', 'location.parent.parent.parent.parent.parent.parent.name', 
            'location.parent.parent.parent.parent.parent.name', 'location.parent.parent.parent.parent.name', 
            'location.parent.parent.parent.name', 
            'location.parent.parent.name', 'location.parent.name', 'location.name',
            'response.A', 'response.B', 'response.CA', 'response.CB', 'response.CC', 'response.CD', 'response.CE', 
            'response.CF', 'response.CG', 'response.CH', 'response.D', 'response.E', 'response.EA',
            'response.EB', 'response.EC', 'response.F', 'response.G', 'response.H', 'response.J', 'response.K',
            'response.M', 'response.N', 'response.P', 'response.Q', 'response.R', 'response.S',
            'response.T', 'response.U', 'response.V', 'response.W', 'response.X', 'response.Y', 'response.Z', 
            'response.AA', 'response.AB', 'response.AC', 'response.AD', 
            'response.AEAA', 'response.AEAB', 'response.AEBA', 'response.AEBB', 'response.AECA', 'response.AECB', 
            'response.AEDA', 'response.AEDB', 'response.AEEA', 'response.AEEB',
            'response.AGA', 'response.AHA', 'response.AJA', 'response.AKA', 'response.AMA', 'response.ANA', 'response.APA', 'response.AQA', 'response.ARA', 'response.ASA', 'response.ATA', 'response.AUA', 
            'response.AGB', 'response.AHB', 'response.AJB', 'response.AKB', 'response.AMB', 'response.ANB', 'response.APB', 'response.AQB', 'response.ARB', 'response.ASB', 'response.ATB', 'response.AUB',  
            'response.AV', 'response.AW', 'response.AX', 'response.AY']
    else:
        # write row header
        columns = ['PDID', 'Monitor Name', 'Monitor Phone', 'Time', 'Province', 'District', 'Constituency', 'Ward', 
            'Polling District', 'Polling Station', 'Polling Stream',
            '1', '2', '3a', '3b', '3c', '3d', '3e', '3f', '3g', '3h', '4', '5', '5a',
            '5b', '5c', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
            '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', 
            '28a1', '28a2', '28a3', '28a4', '28a5', '28a6', 
            '28b1', '28b2', '28b3', '28b4', '28b5', '28b6', 
            '28c1', '28c2', '28c3', '28c4', '28c5', '28c6', 
            '28d1', '28d2', '28d3', '28d4', '28d5', '28d6', 
            '28e1', '28e2', '28e3', '28e4', '28e5', '28e6',
            '29a1', '29a2', '29a3', '29a4', '29a5', '29a6', 
            '29b1', '29b2', '29b3', '29b4', '29b5', '29b6', 
            '29c1', '29c2', '29c3', '29c4', '29c5', '29c6', 
            '29d1', '29d2', '29d3', '29d4', '29d5', '29d6', 
            '29e1', '29e2', '29e3', '29e4', '29e5', '29e6', 
            '29f1', '29f2', '29f3', '29f4', '29f5', '29f6', 
            '29g1', '29g2', '29g3', '29g4', '29g5', '29g6', 
            '29h1', '29h2', '29h3', '29h4', '29h5', '29h6', 
            '29i1', '29i2', '29i3', '29i4', '29i5', '29i6', 
            '29j1', '29j2', '29j3', '29j4', '29j5', '29j6', 
            '29k1', '29k2', '29k3', '29k4', '29k5', '29k6', 
            '29l1', '29l2', '29l3', '29l4', '29l5', '29l6', 
            '29m1', '29m2', '29m3', '29m4', '29m5', '29m6', 
            '29n1', '29n2', '29n3', '29n4', '29n5', '29n6', 
            '30', '31', '32', '33']
    
        data_fields = ['location.parent.code', 'response.monitor_name', 'response.monitor_phone', 
            'response.updated', 'location.parent.parent.parent.parent.parent.parent.name', 
            'location.parent.parent.parent.parent.parent.name', 'location.parent.parent.parent.parent.name', 
            'location.parent.parent.parent.name', 
            'location.parent.parent.name', 'location.parent.name', 'location.name',
            'response.A', 'response.B', 'response.CA', 'response.CB', 'response.CC', 'response.CD', 'response.CE', 
            'response.CF', 'response.CG', 'response.CH', 'response.D', 'response.E', 'response.EA',
            'response.EB', 'response.EC', 'response.F', 'response.G', 'response.H', 'response.J', 'response.K',
            'response.M', 'response.N', 'response.P', 'response.Q', 'response.R', 'response.S',
            'response.T', 'response.U', 'response.V', 'response.W', 'response.X', 'response.Y', 'response.Z', 
            'response.AA', 'response.AB', 'response.AC', 'response.AD', 
            'response.AEAA', 'response.AEAB', 'response.AEAC', 'response.AEAD', 'response.AEAE', 'response.AEAF', 
            'response.AEBA', 'response.AEBB', 'response.AEBC', 'response.AEBD', 'response.AEBE', 'response.AEBF', 
            'response.AECA', 'response.AECB', 'response.AECC', 'response.AECD', 'response.AECE', 'response.AECF', 
            'response.AEDA', 'response.AEDB', 'response.AEDC', 'response.AEDD', 'response.AEDE', 'response.AEDF', 
            'response.AEEA', 'response.AEEB', 'response.AEEC', 'response.AEED', 'response.AEEE', 'response.AEEF',
            'response.AFAA', 'response.AFAB', 'response.AFAC', 'response.AFAD', 'response.AFAE', 'response.AFAF',
            'response.AFBA', 'response.AFBB', 'response.AFBC', 'response.AFBD', 'response.AFBE', 'response.AFBF',
            'response.AFCA', 'response.AFCB', 'response.AFCC', 'response.AFCD', 'response.AFCE', 'response.AFCF',
            'response.AFDA', 'response.AFDB', 'response.AFDC', 'response.AFDD', 'response.AFDE', 'response.AFDF',
            'response.AFEA', 'response.AFEB', 'response.AFEC', 'response.AFED', 'response.AFEE', 'response.AFEF',
            'response.AFFA', 'response.AFFB', 'response.AFFC', 'response.AFFD', 'response.AFFE', 'response.AFFF',
            'response.AFGA', 'response.AFGB', 'response.AFGC', 'response.AFGD', 'response.AFGE', 'response.AFGF',
            'response.AFHA', 'response.AFHB', 'response.AFHC', 'response.AFHD', 'response.AFHE', 'response.AFHF',
            'response.AFJA', 'response.AFJB', 'response.AFJC', 'response.AFJD', 'response.AFJE', 'response.AFJF',
            'response.AFKA', 'response.AFKB', 'response.AFKC', 'response.AFKD', 'response.AFKE', 'response.AFKF',
            'response.AFMA', 'response.AFMB', 'response.AFMC', 'response.AFMD', 'response.AFME', 'response.AFMF',
            'response.AFNA', 'response.AFNB', 'response.AFNC', 'response.AFND', 'response.AFNE', 'response.AFNF',
            'response.AFPA', 'response.AFPB', 'response.AFPC', 'response.AFPD', 'response.AFPE', 'response.AFPF',
            'response.AFQA', 'response.AFQB', 'response.AFQC', 'response.AFQD', 'response.AFQE', 'response.AFQF',
            'response.AG', 'response.AH', 'response.AJ', 'response.AK']
    
    for i, column in enumerate(columns):
        ws.write(0, i, column)

    for row, checklist in enumerate(obj_list):
        for j, field in enumerate(data_fields):
            exec 'value = checklist.%s' % field
            ws.write(row+1, j, unicode(value))
    
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=checklist_export-%d%02d%02d-%02d%02d.xls' % \
        (datetime.today().year, datetime.today().month, datetime.today().day, datetime.today().hour, datetime.today().minute)

    wb.save(response)
    return response

@login_required
@permission_required('webapp.can_export')
def export_incidents(request):
    request_params = request.GET
    resource = IncidentsResource()
    
    applicable_filters = resource.build_filters(request_params)
    obj_list = list(resource.apply_filters(request, applicable_filters))
    
    wb = Workbook()
    ws = wb.add_sheet('Incidents');
    
    if settings.ZAMBIA_DEPLOYMENT == 'RRP':
        # write row header
        columns = ['PDID', 'Monitor Id', 'Time', 'Province', 'District', 'Constituency', 'Ward', 
            'Polling District', 'Polling Station', 'Polling Stream',
            '1', '2a', '2b', '2c', '2d', '2e', '2f', '2g', '2h', '2i', '2j', '2k',
            '2k1', '2k2', '2k4', '2l', '2m', '2n', '2o', '3']
    
        data_fields = ['location.parent.code', 'observer.observer_id', 'response.updated', 'location.parent.parent.parent.parent.parent.parent.name', 
            'location.parent.parent.parent.parent.parent.name', 'location.parent.parent.parent.parent.name', 
            'location.parent.parent.parent.name', 
            'location.parent.parent.name', 'location.parent.name', 'location.name',
            'response.W', 'response.A', 'response.B', 'response.C', 'response.D', 'response.E', 'response.F', 
            'response.G', 'response.H', 'response.I', 'response.J', 'response.K', 'response.K1',
            'response.K2', 'response.K4', 'response.L', 'response.M', 'response.N', 'response.O', 'response.description']
    else:
        # write row header
        columns = ['PDID', 'Monitor Name', 'Monitor Phone', 'Time', 'Province', 'District', 'Constituency', 'Ward', 
            'Polling District', 'Polling Station', 'Polling Stream',
            '1', '2a', '2b', '2c', '2d', '2e', '2f', '2g', '2h', '2i', '2j', '2k',
            '2k1', '2k2', '2k4', '2l', '2m', '2n', '2o', '3']
    
        data_fields = ['location.parent.code', 'response.monitor_name', 'response.monitor_phone', 'updated', 'location.parent.parent.parent.parent.parent.parent.name', 
            'location.parent.parent.parent.parent.parent.name', 'location.parent.parent.parent.parent.name', 
            'location.parent.parent.parent.name', 
            'location.parent.parent.name', 'location.parent.name', 'location.name',
            'response.W', 'response.A', 'response.B', 'response.C', 'response.D', 'response.E', 'response.F', 
            'response.G', 'response.H', 'response.I', 'response.J', 'response.K', 'response.K1',
            'response.K2', 'response.K4', 'response.L', 'response.M', 'response.N', 'response.O', 'response.description']
    
    for i, column in enumerate(columns):
        ws.write(0, i, column)

    for row, incident in enumerate(obj_list):
        for j, field in enumerate(data_fields):
            exec 'value = incident.%s' % field
            ws.write(row+1, j, str(value))
    
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=incident_export-%d%02d%02d-%02d%02d.xls' % \
        (datetime.today().year, datetime.today().month, datetime.today().day, datetime.today().hour, datetime.today().minute)

    wb.save(response)
    return response

@login_required
@permission_required('webapp.can_analyse')
def process_analysis(request):
    if request.POST:
        request_params = request.POST.copy()
        sample = request.POST.get('sample', None)
    else:
        request_params = {}
        sample = None
    
    context = {'title': 'Elections Process Analysis'}
    # remove empty parameters
    for key in request_params.keys():
        if not request_params.get(key):
            del request_params[key]
        
    resource = ChecklistsResource()
    applicable_filters = resource.build_filters(request_params)
            
    if sample:
        if applicable_filters.has_key('location__id__in'):
            applicable_filters['location__id__in'] = [int(id) for id in list(set(Sample.objects.filter(sample=sample).values_list('location__pk', flat=True)) & set(applicable_filters['location__id__in']))]
        else:
            applicable_filters['location__id__in'] = [int(id) for id in Sample.objects.filter(sample=sample).values_list('location__pk', flat=True)]
    
    # remove empty attributes
    for key in applicable_filters.keys():
        if applicable_filters.get(key) == []:
            del applicable_filters[key]
        
    query = ",".join(['%s=%s' % (key, applicable_filters[key]) for key in applicable_filters.keys()])
    
    if query:
        exec 'q = Q(%s)' % query
    else:
        q = Q()
    
    location_id = request.POST.get('location__id', None)
    if location_id:
        context['location'] = Location.objects.get(pk=location_id)
    else:
        context['location'] = Location.objects.get(name="Zambia",type__name="Country")
        
    context['total'] = checklist_N(q)
    
    context['A'] = checklist_Q_options('A', q)
    context['B'] = checklist_Q_options('B', q)
    context['CA'] = checklist_Q_options('CA', q)
    context['CB'] = checklist_Q_options('CB', q)
    context['CC'] = checklist_Q_options('CC', q)
    context['CD'] = checklist_Q_options('CD', q)
    context['CE'] = checklist_Q_options('CE', q)
    context['CF'] = checklist_Q_options('CF', q)
    context['CG'] = checklist_Q_options('CG', q)
    context['CH'] = checklist_Q_options('CH', q)
    context['EA'] = checklist_Q_options('EA', q)
    context['EB'] = checklist_Q_options('EB', q)
    context['EC'] = checklist_Q_options('EC', q)
    context['F'] = checklist_Q_options('F', q)
    context['G'] = checklist_Q_options('G', q)
    context['K'] = checklist_Q_options('K', q)
    context['M'] = checklist_Q_options('M', q)
    context['N'] = checklist_Q_options('N', q)
    context['P'] = checklist_Q_options('P', q)
    context['Q'] = checklist_Q_options('Q', q)
    context['R'] = checklist_Q_options('R', q)
    context['S'] = checklist_Q_options('S', q)
    context['T'] = checklist_Q_options('T', q)
    context['U'] = checklist_Q_options('U', q)
    context['V'] = checklist_Q_options('V', q)
    context['W'] = checklist_Q_options('W', q)
    context['X'] = checklist_Q_options('X', q)
    context['Y'] = checklist_Q_options('Y', q)
    context['Z'] = checklist_Q_options('Z', q)
    context['AA'] = checklist_Q_options('AA', q)
    context['AB'] = checklist_Q_options('AB', q)
    context['AC'] = checklist_Q_options('AC', q)
    context['AD'] = checklist_Q_options('AD', q)
    
    if settings.ZAMBIA_DEPLOYMENT == 'RRP':
        context['AV'] = checklist_Q_options('AV', q)
        context['AW'] = checklist_Q_options('AW', q)
        context['AX'] = checklist_Q_options('AX', q)
        context['AY'] = checklist_Q_options('AY', q)
    else:
        context['AG'] = checklist_Q_options('AG', q)
        context['AH'] = checklist_Q_options('AH', q)
        context['AJ'] = checklist_Q_options('AJ', q)
        context['AK'] = checklist_Q_options('AK', q)
    
    context['D'] = checklist_Q_mean('D', q)
    context['E'] = checklist_Q_mean('E', q)
    context['H'] = checklist_Q_mean('H', q)
    
    context.update({'settings': settings})
        
    return render_to_response('zambia/process_analysis.html', RequestContext(request, context))

@login_required
@permission_required('webapp.can_analyse')
def results_analysis(request):
    context = {'title': 'Elections Results Analysis'}
    context.update({'settings': settings})
    return render_to_response('zambia/results_analysis.html', RequestContext(request, context))

@login_required
@permission_required('webapp.can_analyse')
def station_status(request):
    context = {'title': 'Station Status'}
    location_id = request.POST.get('location__id', None)
    sample = request.POST.get('sample', None)
    
    where_we_at = Location.objects.get(pk=location_id if location_id else 1)
    locations = [str(value) for value in Location.objects.get(pk=location_id if location_id else 1).get_descendants(include_self=True).filter(type__name="Polling Station").values_list('id', flat=True)]
    if not sample:
        locations = list(set(locations) & set([str(value) for value in Sample.objects.all().values_list('location__parent__id', flat=True)]))
    else:
        locations = list(set(locations) & set([str(value) for value in Sample.objects.filter(sample=sample).values_list('location__parent__id', flat=True)]))
        
    stream_stats = stream_status_calc()
    station_data = []
    for location in locations:
        station_data.append({
            'pdid': stream_stats['stream_completion'][location]['code'],
            'name': stream_stats['stream_completion'][location]['name'],
            'total': stream_stats['stream_completion'][location]['total_streams'],
            'stream_in': stream_stats['stream_completion'][location]['stream_count'],
            'station_in': stream_stats['station_completion'][location]['stream_count'],
            'match_no': stream_stats['station_match'][location]['match_count'],
            'sum_no': stream_stats['station_sum'][location]['matches']
        })
    
    context.update({'stations': station_data, 'location': where_we_at, 'settings': settings})
    return render_to_response('zambia/stream_status.html', RequestContext(request, context))
    
def app_templates(context):
    return render_to_string('zambia/templates.html', {}, context)