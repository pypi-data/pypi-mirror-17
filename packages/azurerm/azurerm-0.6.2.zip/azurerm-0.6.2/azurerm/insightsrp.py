"""
Copyright (c) 2016, Guy Bowerman
Description: Simple Azure Resource Manager Python library
License: MIT (see LICENSE.txt file for details)
"""

# insightsrp.py - azurerm functions for the Microsoft.Insights resource provider

from .restfns import do_get
from .settings import azure_rm_endpoint, INSIGHTS_API


# list_autoscale_settings(access_token, subscription_id)
# list the autoscale settings in a subscription_id
def list_autoscale_settings(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/providers/microsoft.insights/',
                        '/autoscaleSettings?api-version=', INSIGHTS_API])
    return do_get(endpoint, access_token)


# list_insights_components(access_token, subscription_id, resource_group)
# list the Microsoft Insights components in a resource group	
def list_insights_components(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', resource_group,
                        '/providers/microsoft.insights/',
                        '/components?api-version=', INSIGHTS_API])
    return do_get(endpoint, access_token)
