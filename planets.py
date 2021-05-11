import ephem

p1 = ephem.EarthSatellite()
p2 = ephem.Saturn()

observer = ephem.Observer()
observer.date = ephem.date('2021/05/03')

p1.compute(observer)
p2.compute(observer)

print(ephem.separation(p1, p2))
print(ephem.next_full_moon('2021/05/11'))