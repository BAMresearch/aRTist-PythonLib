# Copyright 2023 TH DEGGENDORF (contact simon.wittl@th-deg.de)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from pathlib import Path


__SaRTistPath__ = Path(__file__).parent.parent
__SaRTistTCL__ = __SaRTistPath__ / "sartist" / "SaRTist.tcl"
__SaRTistTemp__ = __SaRTistPath__ / "data"

host_send = '127.0.0.1'
port_send = 3658

__send__ = (host_send, port_send)

host_receive = "127.0.0.1"
port_receive = 1234

__receive__ = (host_receive, port_receive)

host_local = "127.0.0.6"
port_local = 0

__local__ = (host_local, port_local)



