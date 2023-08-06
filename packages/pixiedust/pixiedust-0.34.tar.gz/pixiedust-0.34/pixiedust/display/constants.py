# -------------------------------------------------------------------------------
# Copyright IBM Corp. 2016
# 
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------------
from collections import OrderedDict
class ActionCategories(object):
    TABLE = "Table"
    MAP = "Map"
    CHART = "Chart"
    GRAPH = "Graph"

    CAT_INFOS = OrderedDict([
        (TABLE, {"title": "Table", "icon-class": "fa-table"}),
        (CHART, {"title": "Chart", "icon-class": "fa-line-chart"}),
        (MAP,   {"title": "Map", "icon-class": "fa-map"}),
        (GRAPH, {"title": "Graph", "icon-class": "fa-share-alt"})
    ])