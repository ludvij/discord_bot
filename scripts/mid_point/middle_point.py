from geopy import Nominatim


def parse_line(line:str) -> dict:
	if not line.strip(): return
	if '#' in line: return
	parts = line.split('\t')
	res = dict()
	res["name"] = parts[0].lower()
	
	res["x"] = float(parts[1])
	res["y"] = float(parts[2])

	return res


def read_points(filename:str) -> list:
	with open(filename, mode='r', encoding='utf-8') as f:
		points =  [parse_line(x) for x in f.readlines()]
		return [x for x in points if x]


def avg_points(points:list) -> dict:
	n:int = len(points)
	res = dict()
	res["name"] = "average distance"
	res["x"] = sum([x["x"] for x in points if x]) / n
	res["y"] = sum([x["y"] for x in points if x]) / n
	return res





def fmt_placemarks(points:list, color:str='#blue') -> str:
	fmt = '\n'.join([
		'\t<Placemark>',
		'\t\t<name>{name}</name>',
		'\t\t<styleUrl>#{color}</styleUrl> ',

		'\t\t<Point>',
		'\t\t\t<coordinates>{x},{y},0</coordinates>',
		'\t\t</Point>',
		'\t</Placemark>'
	])

	return '\n'.join(
		[fmt.format(name=x["name"], color=color, x=x["x"], y=x["y"]) for x in points if x]
	)

def fmt_colors(colors:list) -> str:
	fmt = '\n'.join([
		'\t<Style id="{color}">',
  		'\t\t<IconStyle>',
    	'\t\t\t<Icon>',
      	'\t\t\t\t<href>http://www.google.com/intl/en_us/mapfiles/ms/icons/{color}-dot.png</href>',
    	'\t\t\t</Icon>',
  		'\t\t</IconStyle>',
		'\t</Style>'
	])

	return '\n'.join(
		[fmt.format(color=x) for x in colors]
	)


def fmt_kml(points:list) -> str:
	fmt = '\n'.join([
		'<?xml version="1.0" encoding="UTF-8"?>',
		'<kml xmlns="http://www.opengis.net/kml/2.2">',
		'<Document>',
		'{colors}',
		'{placemarks}',
		'{average}',
		'</Document>',
		'</kml>'
	])

	avg = list()
	avg.append(avg_points(points))

	return fmt.format(
		colors=fmt_colors(["red", "blue"]),
		placemarks=fmt_placemarks(points, 'blue'), 
		average=fmt_placemarks(avg, "red")
	)

def get_mid_point(users:list) -> tuple:
	with open("rcs/points.txt", mode='r', encoding='utf-8') as f:
		points = [parse_line(x) for x in f.readlines()]
		points = [x for x in points if x]

	res = list()
	for user in users:
		if user.lower() not in [x["name"] for x in points]:
			raise NameError('invalid name')
		
		for x in points:
			if x["name"] == user.lower():
				res.append(x)
				break

	avg = avg_points(res)
	geolocator = Nominatim(user_agent="mid_point")
	location = geolocator.reverse(f"{avg['y']}, {avg['x']}")
	return location.address
	

def main():
	res = read_points("datos.txt")

	kml:str = fmt_kml(res)

	with open("res.kml", "w", encoding="utf-8") as f:
		[f.writelines(kml)]


if __name__ == '__main__':
	main()