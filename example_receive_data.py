
import aRTist as a
import base64

rc = a.Connection()

ch = a.Connection.send(rc, ['::RemoteControl::GetCurrentChannel\n'])[0]

# send string "qwer" as data from aRTist to Python
rdata = a.Connection.send(rc, ['::RemoteControl::SendData '+ch+' "qwer";\n'], '*')[0]
print('<1>'+rdata+'<1>')
rdata_b64 = a.Connection.result(rc, rdata, 'BASE64')
print('<2>'+rdata_b64+'<2>')
rdata_txt = str(base64.b64decode(rdata_b64), 'utf-8')
print('<3>'+rdata_txt+'<3>')

# reduce the viewer image width just to have a tiny image for the example
a.Connection.send(rc, [
  'set Xsetup_private(DGauto) Resolution\n',
  'set Xsetup(DetectorPixelX) 10\n',
  'XDetector::UpdateGeometry $::XDetector::widget(XPixel)\n'
])

# send aRTist viewer image to Python
a_img = a.Connection.send(rc, ['::Modules::Invoke ImageViewer GetCurrentImage\n'])[0]
print('<4>'+a_img+'<4>')
idata = a.Connection.send(rc, ['::RemoteControl::SendImage '+a_img+';\n'], '*')[0]
print('<5>'+idata+'<5>')
# Attention: Larger images will result in multiple BASE64 lines, but so far aRTist.Connection.result() returns the first line only.

