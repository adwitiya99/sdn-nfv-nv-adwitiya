from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # ==========================Agniswar=========================
    path('', views.login, name='login'),
    path('logincontroller/', views.logincontroller, name='logincontroller'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.home, name='home'),

    path('userconfig/', views.userconfig, name='userconfig'),
    path('usercreatecontroller/', views.usercreatecontroller, name='usercreatecontroller'),
    path('logview/', views.viewlog, name='logview'),
    path('userdelete/<int:id>', views.userdelete, name='userdelete'),
    # ==========================Agniswar=========================

    path('graph/visjs/<int:parent_id>/', views.get_graph_visjs, name='getgraphvisjs'),
    path('graph/hierarchical/<int:parent_id>/', views.get_graph_hierarchical, name='getgraphhierarchical'),
    path('graph/node/delete/<int:node_id>/', views.delete_node, name='deletenode'),
    path('graph/node/properties/<int:node_id>/', views.get_properties, name='getnodeproperties'),
    path('networks/', views.get_networks, name='getnetworks'),
    path('network/create/', views.create_network, name='createnetwork'),
    path('network/import/', views.import_network_api, name='importnetwork'),
    path('controllers/<int:parent_id>/', views.get_controllers, name='getcontrollers'),
    path('controller/create/', views.create_controller, name='createcontroller'),
    path('switches/<int:parent_id>/', views.get_switches, name='getswitches'),
    path('switch/create/', views.create_switch, name='createswitch'),
    path('routers/<int:parent_id>/', views.get_routers, name='getrouters'),
    path('router/create/', views.create_router, name='createsrouter'),
    path('hosts/<int:parent_id>/', views.get_hosts, name='gethosts'),
    path('host/create/', views.create_host, name='createhost'),
    path('nodes/<int:network_id>/<str:node_type>/', views.get_nodes_under_network, name='getnodesundernetwork'),

    path('showsdn/', views.showsdn, name='sdn'),

    path('managenetwork/', views.managenetwork, name='managenetwork'),

    path('networkconfig/', views.networkconfig, name='networkconfig'),
    path('config/policy/', views.policy_config, name='policyconfig'),
    path('config/policy/add/', views.add_core_policy_api, name='createpolicy'),
    path('config/policy/<int:id>/', views.update_core_policy_page, name='editpolicypage'),
    path('config/policy/<int:id>/update/', views.update_core_policy_api, name='updatepolicy'),
    path('config/policy/<int:id>/activate/', views.activate_core_policy_api, name='activatepolicy'),
    path('config/policy/<int:id>/deactivate/', views.deactivate_core_policy_api, name='deactivatepolicy'),

    path('reportconfig/', views.reportconfig, name='reportconfig'),
    path('evidenceconfig/', views.evidenceconfig, name='evidenceconfig'),

    # ================== Adwitiya ============================

    path('shownfv/', views.shownfv, name='nfv'),
    path('calculatecost', views.calculatecost, name='calculatecost'),
    path('calculatecostsecond', views.calculatecostsecond, name='calculatecostsecond'),
    path('pingcontroller/', views.pingcontroller, name='pingcontroller'),
    path('createvni/', views.createvni, name='createvni'),
    path('importvnifromfile/', views.importvnifromfile, name='importvnifromfile'),

    path('graph/vnivisjs/<str:parent_name>/', views.get_graph_vnivisjs, name='getgraphvnivisjs'),
    path('createvnilink/', views.createvnilink, name='createvnilink'),
    path('shownv/', views.shownv, name='nv'),
    path('createnvi/', views.createnvi, name='createnvi'),
    path('importnvifromfile/', views.importnvifromfile, name='importnvifromfile'),
    path('createnvilink/', views.createnvilink, name='createnvilink'),
    path('updatenode/', views.updatenode, name='updatenode'),
    path('deletenode/<int:node_id>/', views.deletenode, name='deletenode'),
    # ================== Adwitiya ============================
]
