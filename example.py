
import aRTist as a

rc = a.Connection()

ver = a.Connection.send(rc, ['::aRTist::GetVersion;\n'])[0]
print(ver)

# write at aRTist Console
cmd = 'puts "aRTist ' + ver + ' remote controlled by >>>example.py<<<."\n'
a.Connection.send(rc, [cmd])
print('Some text written to aRTist\'s console.')