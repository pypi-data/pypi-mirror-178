# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkalidns.endpoint import endpoint_data

class DescribePdnsThreatLogsRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Alidns', '2015-01-09', 'DescribePdnsThreatLogs','alidns')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_ThreatSourceIp(self): # String
		return self.get_query_params().get('ThreatSourceIp')

	def set_ThreatSourceIp(self, ThreatSourceIp):  # String
		self.add_query_param('ThreatSourceIp', ThreatSourceIp)
	def get_StartDate(self): # String
		return self.get_query_params().get('StartDate')

	def set_StartDate(self, StartDate):  # String
		self.add_query_param('StartDate', StartDate)
	def get_PageNumber(self): # Long
		return self.get_query_params().get('PageNumber')

	def set_PageNumber(self, PageNumber):  # Long
		self.add_query_param('PageNumber', PageNumber)
	def get_EndDate(self): # String
		return self.get_query_params().get('EndDate')

	def set_EndDate(self, EndDate):  # String
		self.add_query_param('EndDate', EndDate)
	def get_PageSize(self): # Long
		return self.get_query_params().get('PageSize')

	def set_PageSize(self, PageSize):  # Long
		self.add_query_param('PageSize', PageSize)
	def get_ThreatType(self): # String
		return self.get_query_params().get('ThreatType')

	def set_ThreatType(self, ThreatType):  # String
		self.add_query_param('ThreatType', ThreatType)
	def get_Lang(self): # String
		return self.get_query_params().get('Lang')

	def set_Lang(self, Lang):  # String
		self.add_query_param('Lang', Lang)
	def get_Keyword(self): # String
		return self.get_query_params().get('Keyword')

	def set_Keyword(self, Keyword):  # String
		self.add_query_param('Keyword', Keyword)
	def get_ThreatLevel(self): # String
		return self.get_query_params().get('ThreatLevel')

	def set_ThreatLevel(self, ThreatLevel):  # String
		self.add_query_param('ThreatLevel', ThreatLevel)
