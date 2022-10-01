
import os
import artistlib as a

rc = a.Junction()


ver = a.Junction.send(rc, '::aRTist::GetVersion full')
print(ver)

# write out at aRTist's console
cmd = 'puts "aRTist ' + ver + ' remote controlled by >>>' + os.path.basename(__file__) + '<<<."'
a.Junction.send(rc, cmd)
print('Some text written to aRTist\'s console.')