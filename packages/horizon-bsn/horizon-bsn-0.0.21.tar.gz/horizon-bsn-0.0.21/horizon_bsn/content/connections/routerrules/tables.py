# Copyright 2013,  Big Switch Networks, Inc
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from horizon import tables
from horizon_bsn.content.connections.routerrules import rulemanager
from openstack_dashboard import policy

LOG = logging.getLogger(__name__)


class AddRouterRule(policy.PolicyTargetMixin, tables.LinkAction):
    name = "create"
    verbose_name = _("Add Router Policy")
    url = "horizon:project:connections:routerrules:addrouterrule"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "update_router"),)

    def get_link_url(self, datum=None):
        return reverse(self.url)


class RemoveRouterRule(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Router Policy",
            u"Delete Router Policies",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Router Policy",
            u"Deleted Router Policies",
            count
        )

    failure_url = 'horizon:project:connections:index'
    policy_rules = (("network", "update_router"),)

    def delete(self, request, obj_id):
        router_id = self.table.kwargs['router'].id
        rulemanager.remove_rules(request, obj_id,
                                 router_id=router_id)


class RouterRulesTable(tables.DataTable):
    priority = tables.Column("priority", verbose_name=_("Priority"))
    source = tables.Column("source", verbose_name=_("Source CIDR"))
    destination = tables.Column("destination",
                                verbose_name=_("Destination CIDR"))
    action = tables.Column("action", verbose_name=_("Action"))
    nexthops = tables.Column("nexthops", verbose_name=_("Next Hops"))

    def get_object_display(self, rule):
        return "(%(action)s) %(source)s -> %(destination)s" % rule

    def get_object_id(self, datum):
        return datum.priority

    class Meta(object):
        name = "routerrules"
        verbose_name = _("Router Policies")
        table_actions = (AddRouterRule, RemoveRouterRule)
        row_actions = (RemoveRouterRule, )
