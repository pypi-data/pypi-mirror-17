"""
Copyright (c) 2016, Guy Bowerman
Description: Simple Azure Resource Manager Python library
License: MIT (see LICENSE.txt file for details)
"""

# azurerm - library for easy Azure Resource Manager calls from Python

from .adalfns import get_access_token
from .amsrp import list_media_services, list_media_services_rg, list_media_endpoint_keys, \
    check_media_service_name_availability, create_media_service_rg, delete_media_service_rg
from .computerp import delete_vm, get_vm, create_vm, update_vm, list_vms, list_vms_sub, list_as, list_as_sub, \
    list_vm_images_sub, restart_vm, start_vm, stop_vm, deallocate_vm, get_vm_extension, delete_vmss, delete_vmss_vms, \
    get_vmss, update_vmss, get_vmss_instance_view, list_vmss, list_vmss_sub, list_vmss_vms, get_vmss_vm, \
    get_vmss_vm_instance_view, list_vmss_vm_instance_view, get_vmss_nics, get_vmss_vm_nics, start_vmss, \
    stopdealloc_vmss, start_vmss_vms, stopdealloc_vmss_vms, restart_vmss, restart_vmss_vms, poweroff_vmss, \
    poweroff_vmss_vms, reimage_vmss_vms, upgrade_vmss_vms, scale_vmss, get_compute_usage
from .deployments import list_deployment_operations, show_deployment
from .insightsrp import list_insights_components, list_autoscale_settings
from .networkrp import create_nic, create_nsg, create_nsg_rule, create_public_ip, create_vnet, get_lb_nat_rule, \
    get_load_balancer, get_network_usage, get_public_ip, get_vnet, list_load_balancers, list_load_balancers_rg, \
    list_nics, list_nics_rg, list_lb_nat_rules, list_public_ips, list_vnets
from .resourcegroups import create_resource_group, delete_resource_group, list_resource_groups
from .storagerp import create_storage_account, delete_storage_account, get_storage_account, list_storage_accounts_sub, \
    list_storage_accounts_rg, get_storage_usage, get_storage_account_keys
from .subfns import list_locations, list_subscriptions
from .templates import deploy_template, deploy_template_uri, deploy_template_uri_param_uri
from .vmimages import list_offers, list_publishers, list_skus, list_sku_versions
