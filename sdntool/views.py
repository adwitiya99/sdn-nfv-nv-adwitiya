import neo4j.exceptions
import json

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils.safestring import SafeString

from logmanager.manager import ApplicationLogger
from policymanagement.models import PolicyVerificationReport, CorePolicy
from sdntool.models import Usermanagement
from sdntool.formvalidation import Validator
from sdntool.Neo4jcontroller import Neo4JController
from sdntool.Neo4jmodels import required_properties
from sdntool.login_validator import login_check
from sdntool.generator import NameGenerator
from sdntool.utils import import_network, import_vni, extract_required_properties_based_on_requirement, generate_random_id_for_node
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# ========================Login=======================


def login(request):
    return render(request, 'sdntool/index.html')


def logincontroller(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    validator = Validator({
        "username": "required|string",
        "password": "required|string",

    })
    validator.run_validation(request.POST.dict())
    if not validator.valid:
        validator.error_message(request)
        return redirect('login')
    else:
        try:
            user = Usermanagement.objects.get(username=username)
        except Usermanagement.DoesNotExist:
            user = None
        if user is not None:
            if check_password(password, user.password):
                request.session["login"] = {
                    "username": user.username,
                    "loginc": True,
                    "userrole": user.userrole,
                }
                return redirect('home')
            else:
                messages.error(request, "Your password is not correct", extra_tags='loginerror')
                return redirect('login')
        else:
            messages.error(request, "User does not exists", extra_tags='loginerror')
            return redirect('login')


def logout(request):
    del request.session["login"]
    return redirect('login')


@require_GET
@login_check
def get_graph_visjs(request, parent_id):
    try:
        graph = Neo4JController.get_graph(parent_id, format=Neo4JController.VisJSFormat)
        return JsonResponse({
            "success": True,
            "message": "Graph fetched successfully",
            "data": graph
        }, safe=False)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Failed to fetch graph",
            "data": ""
        }, safe=False)


@require_GET
@login_check
def get_graph_hierarchical(request, parent_id):
    try:
        graph = Neo4JController.get_graph(parent_id, format=Neo4JController.HierarchicalFormat)
        return JsonResponse({
            "success": True,
            "message": "Graph fetched successfully",
            "data": graph
        }, safe=False)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Failed to fetch graph",
            "data": ""
        }, safe=False)


@require_GET
@login_check
def get_networks(request):
    networks = Neo4JController.get_networks()
    networks_json = [x.to_json() for x in networks]
    return JsonResponse({
        "success": True,
        "message": "Total {} networks found".format(len(networks)),
        "data": networks_json
    }, safe=False)


@require_POST
@login_check
def create_network(request):
    try:
        name = NameGenerator.get_next_network_name()
        network = Neo4JController.create_network(name, properties={})
        return JsonResponse({
            "success": True,
            "message": "Network created successfully",
            "data": network.to_json()
        })
    except neo4j.exceptions.ConstraintError:
        return JsonResponse({
            "success": False,
            "message": "Failed ! Network already exists"
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Network creation failed due to unexpected reason",
            "data": {}
        })


@require_POST
@login_check
def import_network_api(request):
    try:
        body = json.loads(request.body)
        if "controller" not in body or "switch" not in body or "host" not in body or "link" not in body:
            return JsonResponse({
                "success": False,
                "message": "Invalid request body"
            })
        network = import_network(Neo4JController, NameGenerator, body["controller"], body["switch"],
                                 body["host"], body["link"])
        return JsonResponse({
            "success": True,
            "message": "Network imported successfully",
            "data": network.to_json()
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Network import failed due to unexpected reason",
            "data": {}
        })


@require_GET
@login_check
def get_controllers(request, parent_id: int):
    controllers = Neo4JController.get_controllers(parent_id)
    controllers_json = [x.to_json() for x in controllers]
    return JsonResponse({
        "success": True,
        "message": "Total {} controllers found".format(len(controllers)),
        "data": controllers_json
    }, safe=False)


@require_POST
@login_check
def create_controller(request):
    try:
        parent_id = int(request.POST.get("parent_id"))
        name = NameGenerator.get_next_controller_name()
        properties = extract_required_properties_based_on_requirement(request.POST, required_properties["controller"])
        controller = Neo4JController.create_controller(parent_id, name, properties)
        return JsonResponse({
            "success": True,
            "message": "Controller created successfully",
            "data": controller.to_json()
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Controller creation failed due to unexpected reason",
            "data": {}
        })


@require_GET
@login_check
def get_switches(request, parent_id: int):
    switches = Neo4JController.get_switches(parent_id)
    switches_json = [x.to_json() for x in switches]
    return JsonResponse({
        "success": True,
        "message": "Total {} switches found".format(len(switches)),
        "data": switches_json
    }, safe=False)


@require_POST
@login_check
def create_switch(request):
    try:
        parent_id = int(request.POST.get("parent_id"))
        name = NameGenerator.get_next_switch_name()
        properties = extract_required_properties_based_on_requirement(request.POST, required_properties["switch"])
        switch = Neo4JController.create_switch(parent_id, name, properties)
        return JsonResponse({
            "success": True,
            "message": "Switch created successfully",
            "data": switch.to_json()
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Switch creation failed due to unexpected reason",
            "data": {}
        })


@require_GET
@login_check
def get_routers(request, parent_id: int):
    routers = Neo4JController.get_routers(parent_id)
    routers_json = [x.to_json() for x in routers]
    return JsonResponse({
        "success": True,
        "message": "Total {} routers found".format(len(routers)),
        "data": routers_json
    }, safe=False)


@require_POST
@login_check
def create_router(request):
    try:
        parent_id = int(request.POST.get("parent_id"))
        name = NameGenerator.get_next_router_name()
        properties = extract_required_properties_based_on_requirement(request.POST, required_properties["router"])
        router = Neo4JController.create_router(parent_id, name, properties)
        return JsonResponse({
            "success": True,
            "message": "Router created successfully",
            "data": router.to_json()
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Router creation failed due to unexpected reason",
            "data": {}
        })


@require_GET
@login_check
def get_hosts(request, parent_id: int):
    hosts = Neo4JController.get_hosts(parent_id)
    hosts_json = [x.to_json() for x in hosts]
    return JsonResponse({
        "success": True,
        "message": "Total {} hosts found".format(len(hosts)),
        "data": hosts_json
    }, safe=False)


@require_POST
@login_check
def create_host(request):
    try:
        parent_id = int(request.POST.get("parent_id"))
        name = NameGenerator.get_next_host_name()
        properties = extract_required_properties_based_on_requirement(request.POST, required_properties["host"])
        host = Neo4JController.create_host(parent_id, name, properties)
        return JsonResponse({
            "success": True,
            "message": "Host created successfully",
            "data": host.to_json()
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Host creation failed due to unexpected reason",
            "data": {}
        })


@require_GET
@login_check
def get_properties(request, node_id: int):
    properties = Neo4JController.get_properties(node_id)
    if properties is None:
        return JsonResponse({
            "success": False,
            "message": "Failed to get properties",
            "data": {}
        })
    return JsonResponse({
        "success": True,
        "message": "Properties found",
        "data": properties
    })


@require_GET
@login_check
def delete_node(request, node_id):
    try:
        Neo4JController.delete_node(node_id, delete_all_nodes_relationship=True)
        return JsonResponse({
            "success": True,
            "message": "Node deleted successfully",
            "data": {}
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Node deletion failed due to unexpected reason",
            "data": {}
        })


# ================ DASHBOARD CREATION====================================
@login_check
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    data = {
        "networks": Neo4JController.get_networks(),
        "policy_verification_reports": PolicyVerificationReport.objects.all().order_by("-completed_on")[:5]
    }
    return render(request, 'sdntool/home.html', data)


# ========================================================================


# ================ SDN SELECTION====================================
@login_check
def showsdn(request):
    return render(request, 'sdntool/sdn.html')


# ========================================================================


# ================ NV SELECTION====================================
@login_check
def shownv(request):
    return render(request, 'sdntool/nv.html')


# ========================================================================


# ================ NFV SELECTION====================================
@login_check
def shownfv(request):
    vni = Neo4JController.get_vni()
    vni_json = [x.to_json() for x in vni]

    return render(request, 'sdntool/nfv.html',
                  {'networks': vni_json, 'required_properties': SafeString(required_properties)})

@require_POST
@login_check
def createvni(request):
    try:
        name = NameGenerator.get_next_vni_name()
        vni = Neo4JController.create_vni(name, properties={})
        return JsonResponse({
            "success": True,
            "message": "Virtual Network Infrastructure created successfully",
            "data": vni.to_json()
        })
    except neo4j.exceptions.ConstraintError:
        return JsonResponse({
            "success": False,
            "message": "Failed ! Virtual Network Infrastructure already exists"
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Virtual Network Infrastructure creation failed due to unexpected reason",
            "data": {}
        })


@require_POST
@login_check
def importvnifromfile(request):
    try:
        body = json.loads(request.body)
        if "virtualmachine" not in body or "virtualnetworkfunction" not in body  or "virtualnetwork" not in body:
            # or "link" not in body has been removed
            return JsonResponse({
                "success": False,
                "message": "Invalid request body"
            })
        # print(body["virtualnetwork"])
        network = import_vni(Neo4JController, NameGenerator, body["virtualmachine"], body["virtualnetwork"], body["virtualnetworkfunction"], body["link"])
        return JsonResponse({
            "success": True,
            "message": "Network imported successfully",
            "data": network.to_json()
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": e,
            "data": {}
        })


def get_graph_vnivisjs(request, parent_name):
    try:
        graph = Neo4JController.get_graph_vni(parent_name, format=Neo4JController.VisJSFormat)
        return JsonResponse({
            "success": True,
            "message": "Graph fetched successfully",
            "data": json.loads(graph)
        }, safe=False)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": e,
            "data": ""
        }, safe=False)



# ========================================================================


# ================ Network Topology ====================================
@login_check
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def managenetwork(request):
    networks = Neo4JController.get_networks()
    networks_json = [x.to_json() for x in networks]

    return render(request, 'sdntool/managenetwork.html',
                  {'networks': networks_json, 'required_properties': SafeString(required_properties)})


# ========================================================================
# ================ NETWORK CONFIGURATION====================================
def networkconfig(request):
    return render(request, 'sdntool/networkconfig.html')


# ========================================================================


# ================ POLICY CONFIGURATION ====================================
@require_GET
@login_check
def policy_config(request):
    data = {
        "policies": CorePolicy.objects.all()
    }
    return render(request, 'sdntool/policyconfig.html', data)


@require_GET
@login_check
def update_core_policy_page(request, id):
    data = {
        "policy": CorePolicy.objects.get(id=id)
    }
    return render(request, 'sdntool/update_core_policy.html', data)


from django.views.decorators.csrf import csrf_exempt


@require_POST
@csrf_exempt
def add_core_policy_api(request):
    try:
        request_body = json.loads(request.body)
        policy_name = request_body.get("name")
        policy_description = request_body.get("description")
        fields_info = request_body.get("fields_info")
        fields_elements = [field["variable"] for field in fields_info]
        if len(fields_elements) != len(set(fields_elements)):
            return JsonResponse({
                "success": False,
                "message": "Duplicate fields are not allowed",
                "data": {}
            })
        blockly_json = {
            "blocks": {
                "languageVersion": 0,
                "blocks":
                    [
                        {
                            "type": "main_entrypoint",
                            "id": "ukq!tUJ.Wf9q{0HrfHTA",
                            "x": -1016,
                            "y": -578
                        }
                    ]
            },
            "variables": [{"name": x, "id": generate_random_id_for_node()} for x in fields_elements]
        }
        record = CorePolicy.objects.create(
            name=policy_name,
            description=policy_description,
            fields_info=json.dumps(fields_info),
            blockly_json=json.dumps(blockly_json)
        )
        return JsonResponse({
            "success": True,
            "message": "Policy added successfully",
            "data": {
                "id": record.id,
                "name": record.name,
                "description": record.description,
            }
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": "Failed to add policy",
            "data": {}
        })


@require_POST
@login_check
@csrf_exempt
def update_core_policy_api(request, id):
    try:
        request_body = json.loads(request.body)
        blockly_json = request_body.get("blockly_json", {})
        generated_code = request_body.get("generated_code")
        record = CorePolicy.objects.get(id=id)
        record.blockly_json = json.dumps(blockly_json)
        record.generated_code = generated_code
        record.save()
        return JsonResponse({
            "success": True,
            "message": "Policy updated successfully",
            "data": {}
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": "Failed to update policy",
            "data": {}
        })


@require_POST
@login_check
@csrf_exempt
def activate_core_policy_api(request, id):
    try:
        record = CorePolicy.objects.get(id=id)
        record.is_active = True
        record.save()
        return JsonResponse({
            "success": True,
            "message": "Policy re-activated successfully",
            "data": {}
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": "Failed to activate policy",
            "data": {}
        })


@require_POST
@login_check
@csrf_exempt
def deactivate_core_policy_api(request, id):
    try:
        record = CorePolicy.objects.get(id=id)
        record.is_active = False
        record.save()
        return JsonResponse({
            "success": True,
            "message": "Policy deactivated successfully",
            "data": {}
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": "Failed to deactivate policy",
            "data": {}
        })


# ========================================================================

# ================ USER CONFIGURATION ====================================
@login_check
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userconfig(request):
    if (request.session["login"]["userrole"] == "admin"):

        users = Usermanagement.objects.all();
        return render(request, 'sdntool/userconfig.html', {'users': users})
    else:
        return redirect('home')


@login_check
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def usercreatecontroller(request):
    username = request.POST.get("username")
    password = make_password(request.POST.get("password"))
    userrole = request.POST.get("userrole")
    Usermanagement.objects.create(username=username, userrole=userrole, password=password)
    ApplicationLogger.info(
        f"A new user {username} with role {userrole} has been created by {request.session['login']['username']} ")
    messages.success(request, "You have successfully created a user", extra_tags='usercreation')
    return redirect('userconfig')


@login_check
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userdelete(request, id):
    member = Usermanagement.objects.get(idusermanagement=id)
    member.delete()
    return redirect('userconfig')


# ========================================================================

# ================ REPORT CONFIGURATION ====================================
def reportconfig(request):
    return render(request, 'sdntool/reportconfig.html')


# ========================================================================

# ================ EVIDENCE CONFIGURATION ====================================
def evidenceconfig(request):
    return render(request, 'sdntool/evidenceconfig.html')


# ========================================================================
@login_check
def get_nodes_under_network(request, network_id, node_type):
    try:
        nodes = None
        if node_type == "controller":
            nodes = Neo4JController.get_all_controllers_of_network(network_id)
        elif node_type == "switch":
            nodes = Neo4JController.get_all_switches_of_network(network_id)
        elif node_type == "router":
            nodes = Neo4JController.get_all_routers_of_network(network_id)
        elif node_type == "host":
            nodes = Neo4JController.get_all_hosts_of_network(network_id)

        if nodes is None:
            return JsonResponse({
                "success": False,
                "message": "No nodes found",
                "data": {}
            })
        nodes_json = [x.to_json() for x in nodes]
        return JsonResponse({
            "success": True,
            "message": "Total {} nodes found".format(len(nodes)),
            "data": nodes_json
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "message": "Failed to get nodes",
            "data": {}
        })
