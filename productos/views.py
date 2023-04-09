import json
import pandas as pd
import xlwt
#nuevas importaciones 30-05-2022
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from registration.models import Profile

from django.db.models import Count, Avg, Q
from django.shortcuts import render, redirect
from rest_framework import generics, viewsets
from rest_framework.decorators import (
	api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from productos.models import Local, Bodega


# Create your views here.

@login_required
def productos_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'productos/producto_main.html'
    return render(request,template_name,{'profile':profile})

@login_required
def productos_local_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'productos/productos_local_add.html'
    return render(request,template_name,{'profile':profile})

@login_required
def productos_local_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        #se agregan los atributos de la entidad local
        #[id_local,nombre_local,telefono,direccion,encargado,num_bodegas]
        nombre_local = request.POST.get('nombre_local')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        encargado = request.POST.get('encargado')
        num_bodegas = request.POST.get('num_bodegas')

        if nombre_local == '' or telefono == '' or direccion == '' or encargado == '' or num_bodegas == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('productos_local_add')
        producto_local_save = Local(
            nombre_local = nombre_local,
            telefono = telefono,
            direccion = direccion,
            encargado = encargado,
            num_bodegas = num_bodegas,
            )
        #Guardado
        producto_local_save.save()
        messages.add_message(request, messages.INFO, 'Local ingresado con éxito')
        return redirect('productos_list_locales')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def productos_local_ver(request,id_local):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    local_data = Local.objects.get(pk=id_local)
    template_name = 'produtos/productos_local_ver.html'
    return render(request,template_name,{'profile':profile,'local_data':local_data})

@login_required
def productos_list_locales(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if page == None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') == None:
        page = page
    else:
        page = request.GET.get('page') 
    if search == None:
        search = request.GET.get('search')
    else:
        search = search
    if request.GET.get('search') == None:
        search = search
    else:
        search = request.GET.get('search') 
    if request.method == 'POST':
        search = request.POST.get('search') 
        page = None
    h_list = []
    if search == None or search == "None":
        h_count = Local.objects.filter(estado='Activo').count()
        h_list_array = Local.objects.filter(estado='Activo').order_by('id_local')
        for h in h_list_array:
            h_list.append({'id_local':h.id_local,'nombre_local':h.nombre_local,'direccion':h.direccion,'encargado':h.encargado,'num_bodegas':h.num_bodegas})
    else:
        h_count = Local.objects.filter(estado='Activo').filter(nombre_local__icontains=search).count()
        h_list_array = Local.objects.filter(estado='Activo').filter(nombre_local__icontains=search).order_by('nombre_local')
        for h in h_list_array:
            h_list.append({'id_local':h.id_local,'nombre_local':h.nombre_local,'direccion':h.direccion,'encargado':h.encargado,'num_bodegas':h.num_bodegas})            
    paginator = Paginator(h_list, 1) 
    h_list_paginate= paginator.get_page(page)   
    template_name = 'productos/productos_list_locales.html'
    return render(request,template_name,{'template_name':template_name,'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page})

#CARGA MASIVA
@login_required
def import_file(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre Local','Teléfono','Direccion','Encargado','Numero de bodegas']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(2):
            if col_num == 0:
                ws.write(row_num, col_num, 'ej: Sta rosa 1' , font_style)
            if col_num == 1:                           
                ws.write(row_num, col_num, '+56995239244' , font_style)
            if col_num == 2:                           
                ws.write(row_num, col_num, 'San Diego 1975' , font_style)
            if col_num == 3:                           
                ws.write(row_num, col_num, 'Ricardo Meruane' , font_style)
            if col_num == 4:                           
                ws.write(row_num, col_num, '6' , font_style)
    wb.save(response)
    return response 

@login_required
def productos_local_carga_masiva(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'productos/locales_carga_masiva.html'
    return render(request,template_name,{'profiles':profiles})
 
@login_required
def productos_local_carga_masiva_save(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        #try:
        print(request.FILES['myfile'])
        data = pd.read_excel(request.FILES['myfile'])
        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():
            #capturamos los datos desde excel
            nombre_local = str(item[1])            
            telefono = str(item[2])
            direccion = str(item[3])            
            encargado = str(item[4])
            num_bodegas = int(item[5])            

            local_save = Local(
                nombre_local = nombre_local,            
                telefono = telefono,
                direccion = direccion,            
                encargado = encargado,
                num_bodegas = num_bodegas,
                )
            local_save.save()
        messages.add_message(request, messages.INFO, 'Carga masiva finalizada, se importaron '+str(acc)+' registros')
        return redirect('locales_carga_masiva')    
    

#ENDPOINT
#Listar Proveedores Activos
#@api_view(['GET'])
#def product_list_rest(request, format=None):

#@api_view(['POST'])
#def product_edit_rest(request, format=None):

@api_view(['POST'])
def productos_local_add_rest(request, format=None):    
    if request.method == 'POST':
        nombre_local = request.data['nombre_local'] 
        telefono = request.data['telefono'] 
        direccion = request.data['direccion'] 
        encargado = request.data['encargado'] 
        num_bodegas = request.data['num_bodegas'] 

        if nombre_local == '' or telefono == ''or direccion == ''or encargado == ''or num_bodegas == '':
            return Response({'Msj': "Error los datos no pueder estar en blanco"})                         
        local_save = Local(
            nombre_local = nombre_local,
            telefono = telefono,
            direccion = direccion,
            encargado = encargado, 
            num_bodegas = num_bodegas,
            )
        local_save.save()
        return Response({'Msj': "El local ha sido creado"})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['GET'])
def productos_local_list_rest(request, format=None):    
    if request.method == 'GET':
        local_list =  Local.objects.all().order_by('nombre_local')
        local_json = []
        for h in local_list:
            local_json.append({'nombre_local':h.nombre_local,'telefono':h.telefono,'direccion':h.direccion,'encargado':h.encargado,'num_bodegas':h.num_bodegas,'estado':h.estado})
        return Response({'Listado': local_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def productos_local_get_element_rest(request, format=None):    
    if request.method == 'POST':
        local_json = []
        id_local = request.data['id_local']
        local_array =  Local.objects.get(pk=id_local)
        local_json.append(
            {'id_local':local_array.id_local,
             'nombre_local':local_array.nombre_local,
             'telefono':local_array.telefono,
             'encargado':local_array.encargado,
             'num_bodegas':local_array.num_bodegas,
             'estado':local_array.estado
             })
        return Response({local_array.nombre_local:local_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def productos_local_update_element_rest(request, format=None):    
    if request.method == 'POST':
        id_local = request.data['id_local']
        nombre_local = request.data['nombre_local']
        telefono = request.data['telefono']
        encargado = request.data['encargado']
        num_bodegas = request.data['num_bodegas']
        estado = request.data['estado']
        Local.objects.filter(pk=id_local).update(nombre_local=nombre_local)
        Local.objects.filter(pk=id_local).update(telefono=telefono)
        Local.objects.filter(pk=id_local).update(encargado=encargado)
        Local.objects.filter(pk=id_local).update(num_bodegas=num_bodegas)
        Local.objects.filter(pk=id_local).update(estado=estado)
        return Response({'Msj':'Local editado con éxito'})
    else:
        return Response({'Msj': 'Error método no soportado'})

@api_view(['POST'])
def productos_local_del_element_rest(request, format=None):    
    if request.method == 'POST':
        local_id = request.data['local_id']
        Local.objects.filter(pk=local_id).delete()
        return Response({'Msj':'Local eliminado con éxito'})
    else:
        return Response({'Msj': 'Error método no soportado'})

@api_view(['POST'])
def productos_local_list_date_rest(request, format=None):    
    if request.method == 'POST':
        created = request.data['created']
        local_list_count = Local.objects.filter(created=created).count()
        if local_list_count > 0:
            local_list =  Local.objects.filter(created=created).order_by('nombre_local')
            local_json = []
            for h in local_list:
                local_json.append({'nombre_local':h.nombre_local,'telefono':h.telefono,'direccion':h.direccion,'encargado':h.encargado,'num_bodegas':h.num_bodegas,'estado':h.estado})
            return Response({'Listado': local_json})
        else:
            return Response({'Msj': 'No existen locales creados el '+str(created)})
    else:
        return Response({'Msj': 'Error método no soportado'})

@api_view(['POST'])
def productos_local_list_range_date_rest(request, format=None):    
    if request.method == 'POST':
        initial = request.data['initial']
        final = request.data['final']
        local_list_count = Local.objects.filter(created__range=(initial,final)).count()
        if local_list_count > 0:
            local_list =  Local.objects.filter(created__range=(initial,final)).order_by('nombre')
            local_json = []
            for h in local_list:
                local_json.append({'nombre_local':h.nombre_local,'telefono':h.telefono,'direccion':h.direccion,'encargado':h.encargado,'num_bodegas':h.num_bodegas,'estado':h.estado})
            return Response({'Listado': local_json})
        else:
            return Response({'Msj': 'No existen Locales creados entre el '+str(initial)+' al '+str(final)})
    else:
        return Response({'Msj': 'Error método no soportado'})


@api_view(['POST'])
def productos_local_list_contains(request, format=None):    
    if request.method == 'POST':
        search = request.data['search']
        local_list_count = Local.objects.filter(Q(nombre_local__icontains=search)|Q(encargado__icontains=search)).count()
        if local_list_count > 0:
            local_list =  Local.objects.filter(Q(nombre_local__icontains=search)|Q(encargado__icontains=search)).order_by('nombre')
            local_json = []
            for h in local_list:
                local_json.append({'nombre_local':h.nombre_local,'telefono':h.telefono,'direccion':h.direccion,'encargado':h.encargado,'num_bodegas':h.num_bodegas,'estado':h.estado})
            return Response({'Listado': local_json})
        else:
            return Response({'Msj': 'No existen locales que concuerden en nombre o encargado con la cadena '+str(search)})    
    else:
        return Response({'Msj': 'Error método no soportado'})