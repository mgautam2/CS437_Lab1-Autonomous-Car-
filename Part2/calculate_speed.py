import picar_4wd as fc
import time

distance_start = fc.get_distance_at(0)
fc.forward(20)
time.sleep(1)
fc.stop()
distance_end = fc.get_distance_at(0)

print("Start:    " + str(distance_start))
print("End:      " + str(distance_end))

# In cm/s
speed = distance_start - distance_end
print(speed)
