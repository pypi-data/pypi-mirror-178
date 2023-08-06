import string
import random
import platform
import logging
import subprocess
import sys
import traceback

import connexion


def rand_string(length):
    chars = string.ascii_letters + string.punctuation
    return "".join(random.choice(chars) for x in range(20))


def camel2snake(string):
    """
    convert camel case to snake case
    """
    if string is None:
        return None
    new_string = ""
    for c in string:
        if c >= "A" and c <= "Z":
            new_string += "_" + c.lower()
        else:
            new_string += c
    return new_string


def pyVerGt(version: str = "3.9.0") -> bool:
    pyVer = list(map(int, platform.python_version().split(".")))
    version = list(map(int, version.split(".")))
    return pyVer[1] >= version[1]


def portInUse(port: int) -> bool:
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = sock.connect_ex(("localhost", int(port)))
    sock.close()
    return res == 0


class Resolver(connexion.resolver.RestyResolver):
    def resolve_operation_id_using_rest_semantics(self, operation):
        """
        Resolves the operationId using REST semantics
        :type operation: connexion.operations.AbstractOperation
        """

        # Split the path into components delimited by '/'
        path_components = [c for c in operation.path.split("/") if len(c)]

        def is_var(component):
            """True if the path component is a var. eg, '{id}'"""
            return (component[0] == "{") and (component[-1] == "}")

        resource_name = ".".join([c for c in path_components if not is_var(c)]).replace("-", "_")
        if resource_name[-1] == "s":
            resource_name = resource_name[:-1]

        def get_controller_name():
            x_router_controller = operation.router_controller

            name = self.default_module_name

            if x_router_controller:
                name = x_router_controller

            elif resource_name:
                d = self.default_module_name
                r = resource_name
                # name = f"{d}.{r}.controller"
                name = f"{d}.controller.{r}"
            return name

        def get_function_name():
            method = operation.method

            is_collection_endpoint = method.lower() == "get" and len(resource_name) and not is_var(path_components[-1])

            return self.collection_endpoint_name if is_collection_endpoint else method.lower()

        # print(f"{get_controller_name()}.{get_function_name()}")
        return f"{get_controller_name()}.{get_function_name()}"

    # TODO: find a better way to resolve this
    def resolve_operation_id(self, operation):
        # TODO: auto resolve /collection/{item}/collection

        special = {
            "/projects/{project_id}/tasks getTasks": "paddlelabel.api.controller.task.get_by_project",
            "/projects/{project_id}/tasks setAll": "paddlelabel.api.controller.task.set_all_by_project",
            "/projects/{project_id}/labels getLabels": "paddlelabel.api.controller.label.get_by_project",
            "/projects/{project_id}/labels setLabels": "paddlelabel.api.controller.label.set_by_project",
            "/projects/{project_id}/labels removeLabels": "paddlelabel.api.controller.label.delete_by_project",
            "/projects/{project_id}/annotations getAnnotations": "paddlelabel.api.controller.annotation.get_by_project",
            "/projects/{project_id}/tags getTags": "paddlelabel.api.controller.tag.get_by_project",
            "/projects/{project_id}/progress getProgress": "paddlelabel.api.controller.task.get_stat_by_project",
            "/projects/{project_id}/split splitDataset": "paddlelabel.api.controller.project.split_dataset",
            "/projects/{project_id}/export exportDataset": "paddlelabel.api.controller.project.export_dataset",
            "/projects/{project_id}/import importDataset": "paddlelabel.api.controller.project.import_dataset",
            "/projects/{project_id}/predict predict": "paddlelabel.api.controller.project.predict",
            "/projects/{project_id}/toEasydata toEasydata": "paddlelabel.api.controller.project.to_easydata",
            "/tasks/{task_id}/tags getTags": "paddlelabel.api.controller.tag.get_by_task",
            "/tasks/{task_id}/tags addTag": "paddlelabel.api.controller.tag.add_to_task",
            "/datas/{data_id}/image getImage": "paddlelabel.api.controller.data.get_image",
            "/datas/{data_id}/mask getMask": "paddlelabel.api.controller.data.get_mask",
            "/tasks/{task_id}/annotations getAnnotations": "paddlelabel.api.controller.annotation.get_by_task",
            "/tasks/{task_id}/datas getDatas": "paddlelabel.api.controller.data.get_by_task",
            "/datas/{data_id}/annotations getAnnotations": "paddlelabel.api.controller.annotation.get_by_data",
            "/datas/{data_id}/annotations setAnnotations": "paddlelabel.api.controller.annotation.set_all_by_data",
            "/datas/{data_id}/annotations deleteAnnotations": "paddlelabel.api.controller.annotation.delete_by_data",
            "/rpc/folders getFolders": "paddlelabel.api.rpc.file.get_folders",
            "/rpc/seg/polygon2points polygon2points": "paddlelabel.api.rpc.seg.polygon2points_str",
            "/rpc/seg/points2polygon points2polygon": "paddlelabel.api.rpc.seg.points2polygon_str",
            "/rpc/cache createCache": "paddlelabel.api.rpc.cache.create_cache",
            "/rpc/cache/{cache_id} getCache": "paddlelabel.api.rpc.cache.get_cache",
            "/debug/printid/{debug_id} printDebugId": "paddlelabel.api.rpc.debug.cmdOutputDebugId",
            "/version getVersion": "paddlelabel.api.rpc.monitor.get_version",
            "/samples loadSample": "paddlelabel.api.controller.sample.load_sample",
            "/samples/structure getStructure": "paddlelabel.api.controller.sample.sample_folder_structure",
            "/samples/file getFile": "paddlelabel.api.controller.sample.serve_sample_file",
        }
        opid = None

        if operation.operation_id and operation.operation_id.startswith("paddlelabel"):
            opid = operation.operation_id

        path = operation.path
        if path[:-1] == "/":
            path = path[:-1]
        idx = f"{path} {operation.operation_id}"
        if idx in special.keys():
            opid = special[idx]
        # print("resolve resolve resolve", operation.operation_id, path, opid)
        if opid:
            router_controller = operation.router_controller
            if router_controller is None:
                return opid
            return f"{router_controller}.{opid}"

        return self.resolve_operation_id_using_rest_semantics(operation)


def version_check(name="paddlelabel", log=False):
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', f'{name}=='], capture_output=True))
    latest_version = latest_version[latest_version.find('(from versions:')+15:]
    latest_version = latest_version[:latest_version.find(')')]
    latest_version = latest_version.replace(' ','').split(',')[-1]

    current_version = str(subprocess.run([sys.executable, '-m', 'pip', 'show', '{}'.format(name)], capture_output=True))
    current_version = current_version[current_version.find('Version:')+8:]
    current_version = current_version[:current_version.find('\\n')].replace(' ','') 

    if latest_version != current_version:
        return True
    else:
        if log:
            logging.info(f"Currently running {name}=={current_version}, a newer version {latest_version} is avaliable on pypi. Please consider updating {name} with:\n\tpip install --upgrade {name}")
        return False

def backend_error(error):
    """global error handling for backend

    Args:
        error (Exception): Any exception raised

    Returns:
        dict, int: response body, status code
    """    
    print(traceback.format_exc())
    return {
        "title": "Backend error: " + str(error),
        "detail": "Backend error: " + str(error),
        "status": 500,
    }, 500
